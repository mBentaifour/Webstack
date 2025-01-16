import os
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
import requests
from django.conf import settings
from datetime import datetime, timedelta
import json
from decimal import Decimal

class RecommendationAnalysisTests(TestCase):
    """Tests d'intégration et d'analyse pour les recommandations utilisant l'API réelle et Supabase"""
    
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.client = APIClient()
        cls.api_base_url = settings.API_GATEWAY_URL
        cls.supabase_url = settings.SUPABASE_URL
        cls.supabase_key = settings.SUPABASE_KEY
        
        # Authentification avec Supabase
        cls.auth_token = cls._get_auth_token()
        cls.client.credentials(HTTP_AUTHORIZATION=f'Bearer {cls.auth_token}')
        
        # Métriques pour l'analyse
        cls.metrics = {
            'response_times': [],
            'product_counts': [],
            'price_ranges': [],
            'categories_frequency': {},
            'brands_frequency': {}
        }

    @classmethod
    def _get_auth_token(cls):
        """Obtient un token d'authentification depuis Supabase"""
        auth_url = f"{cls.supabase_url}/auth/v1/token?grant_type=password"
        response = requests.post(
            auth_url,
            headers={
                'apikey': cls.supabase_key,
                'Content-Type': 'application/json'
            },
            json={
                'email': os.getenv('TEST_USER_EMAIL'),
                'password': os.getenv('TEST_USER_PASSWORD')
            }
        )
        return response.json().get('access_token')

    def _analyze_products(self, products, context=""):
        """Analyse détaillée des produits retournés"""
        if not products:
            self.fail(f"Aucun produit retourné pour {context}")
            
        analysis = {
            'count': len(products),
            'price_range': {'min': float('inf'), 'max': float('-inf')},
            'categories': {},
            'brands': {},
            'stock_levels': {'low': 0, 'medium': 0, 'high': 0}
        }
        
        for product in products:
            # Vérification de la structure des données
            required_fields = ['id', 'name', 'price', 'stock', 'category', 'brand']
            for field in required_fields:
                self.assertIn(field, product, f"Champ {field} manquant dans {context}")
            
            # Analyse des prix
            price = Decimal(str(product['price']))
            analysis['price_range']['min'] = min(analysis['price_range']['min'], price)
            analysis['price_range']['max'] = max(analysis['price_range']['max'], price)
            
            # Analyse des catégories
            category = product['category']['name']
            analysis['categories'][category] = analysis['categories'].get(category, 0) + 1
            
            # Analyse des marques
            brand = product['brand']['name']
            analysis['brands'][brand] = analysis['brands'].get(brand, 0) + 1
            
            # Analyse des niveaux de stock
            stock = product['stock']
            if stock < 10:
                analysis['stock_levels']['low'] += 1
            elif stock < 50:
                analysis['stock_levels']['medium'] += 1
            else:
                analysis['stock_levels']['high'] += 1
        
        # Mise à jour des métriques globales
        self.metrics['product_counts'].append(analysis['count'])
        self.metrics['price_ranges'].append(analysis['price_range'])
        
        # Mise à jour des fréquences
        for category, count in analysis['categories'].items():
            self.metrics['categories_frequency'][category] = \
                self.metrics['categories_frequency'].get(category, 0) + count
        
        for brand, count in analysis['brands'].items():
            self.metrics['brands_frequency'][brand] = \
                self.metrics['brands_frequency'].get(brand, 0) + count
        
        return analysis

    def test_personalized_recommendations(self):
        """Test et analyse des recommandations personnalisées"""
        start_time = datetime.now()
        response = self.client.get(f"{self.api_base_url}/recommendations/personalized/")
        response_time = (datetime.now() - start_time).total_seconds()
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('products', response.data)
        
        analysis = self._analyze_products(response.data['products'], "recommandations personnalisées")
        
        # Vérifications spécifiques aux recommandations personnalisées
        self.assertGreaterEqual(analysis['count'], 5, "Nombre minimum de recommandations non atteint")
        self.assertLessEqual(analysis['count'], 20, "Trop de recommandations retournées")
        
        # Vérification de la diversité des recommandations
        category_diversity = len(analysis['categories']) / analysis['count']
        brand_diversity = len(analysis['brands']) / analysis['count']
        self.assertGreaterEqual(category_diversity, 0.3, "Diversité des catégories trop faible")
        self.assertGreaterEqual(brand_diversity, 0.3, "Diversité des marques trop faible")
        
        self.metrics['response_times'].append(response_time)

    def test_similar_products(self):
        """Test et analyse des produits similaires"""
        # Obtenir un produit existant
        products_response = requests.get(
            f"{self.supabase_url}/rest/v1/products?select=id,category,price&limit=1",
            headers={'apikey': self.supabase_key}
        )
        reference_product = products_response.json()[0]
        
        start_time = datetime.now()
        response = self.client.get(f"{self.api_base_url}/recommendations/similar/{reference_product['id']}/")
        response_time = (datetime.now() - start_time).total_seconds()
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('products', response.data)
        
        analysis = self._analyze_products(response.data['products'], "produits similaires")
        
        # Vérification de la pertinence des produits similaires
        reference_price = Decimal(str(reference_product['price']))
        price_range = analysis['price_range']
        self.assertLessEqual(
            abs(price_range['min'] - reference_price) / reference_price,
            0.5,
            "Prix minimum trop éloigné du produit de référence"
        )
        self.assertLessEqual(
            abs(price_range['max'] - reference_price) / reference_price,
            0.5,
            "Prix maximum trop éloigné du produit de référence"
        )
        
        self.metrics['response_times'].append(response_time)

    def test_trending_products(self):
        """Test et analyse des produits tendance"""
        start_time = datetime.now()
        response = self.client.get(f"{self.api_base_url}/recommendations/trending/")
        response_time = (datetime.now() - start_time).total_seconds()
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('products', response.data)
        
        analysis = self._analyze_products(response.data['products'], "produits tendance")
        
        # Vérification des caractéristiques des produits tendance
        self.assertGreaterEqual(analysis['count'], 5, "Pas assez de produits tendance")
        self.assertLessEqual(analysis['count'], 15, "Trop de produits tendance")
        
        # Vérification des niveaux de stock
        total_products = sum(analysis['stock_levels'].values())
        high_stock_ratio = analysis['stock_levels']['high'] / total_products
        self.assertGreaterEqual(high_stock_ratio, 0.4, "Proportion insuffisante de produits avec stock élevé")
        
        self.metrics['response_times'].append(response_time)

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        
        # Analyse finale des métriques
        if cls.metrics['response_times']:
            avg_response_time = sum(cls.metrics['response_times']) / len(cls.metrics['response_times'])
            print(f"\nTemps de réponse moyen: {avg_response_time:.3f} secondes")
        
        if cls.metrics['product_counts']:
            avg_products = sum(cls.metrics['product_counts']) / len(cls.metrics['product_counts'])
            print(f"Nombre moyen de produits par requête: {avg_products:.1f}")
        
        if cls.metrics['categories_frequency']:
            print("\nFréquence des catégories:")
            for category, count in sorted(cls.metrics['categories_frequency'].items(), 
                                       key=lambda x: x[1], reverse=True)[:5]:
                print(f"- {category}: {count}")
        
        if cls.metrics['brands_frequency']:
            print("\nFréquence des marques:")
            for brand, count in sorted(cls.metrics['brands_frequency'].items(), 
                                     key=lambda x: x[1], reverse=True)[:5]:
                print(f"- {brand}: {count}")
        
        if cls.metrics['price_ranges']:
            all_min = min(r['min'] for r in cls.metrics['price_ranges'])
            all_max = max(r['max'] for r in cls.metrics['price_ranges'])
            print(f"\nGamme de prix globale: {all_min} - {all_max}")
