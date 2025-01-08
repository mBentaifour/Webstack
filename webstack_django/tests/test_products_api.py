import unittest
import requests
import json
import os
from dotenv import load_dotenv
from datetime import datetime

# Charger les variables d'environnement
load_dotenv()

class TestProductsAPI(unittest.TestCase):
    """Tests pour l'API des produits"""
    
    @classmethod
    def setUpClass(cls):
        """Configuration initiale pour tous les tests"""
        cls.BASE_URL = "http://localhost:8000/api"
        cls.test_product_data = {
            "name": "Produit Test Automatisé",
            "slug": "produit-test-automatise",
            "description": "Produit créé pour les tests automatisés",
            "price": 99.99,
            "stock": 50,
            "category_id": "29bf495e-eb1c-43b1-b753-80a937129628"
        }
        cls.created_products = []

    def setUp(self):
        """Configuration avant chaque test"""
        # Créer un produit pour le test si nécessaire
        response = requests.post(
            f"{self.BASE_URL}/products/",
            json=self.test_product_data
        )
        if response.status_code == 201:
            self.current_product = response.json()
            self.created_products.append(self.current_product['id'])

    def tearDown(self):
        """Nettoyage après chaque test"""
        # Supprimer les produits créés pendant le test
        for product_id in self.created_products:
            requests.delete(f"{self.BASE_URL}/products/{product_id}/")
        self.created_products = []

    def test_01_list_products(self):
        """Test: Récupération de la liste des produits"""
        response = requests.get(f"{self.BASE_URL}/products/")
        self.assertEqual(response.status_code, 200)
        products = response.json()
        self.assertIsInstance(products, list)
        if products:
            self.assertIn('id', products[0])
            self.assertIn('name', products[0])
            self.assertIn('price', products[0])

    def test_02_create_product(self):
        """Test: Création d'un nouveau produit"""
        new_product = {
            "name": "Nouveau Produit Test",
            "slug": "nouveau-produit-test",
            "description": "Description du nouveau produit test",
            "price": 149.99,
            "stock": 30,
            "category_id": "29bf495e-eb1c-43b1-b753-80a937129628"
        }
        
        response = requests.post(f"{self.BASE_URL}/products/", json=new_product)
        self.assertEqual(response.status_code, 201)
        
        created_product = response.json()
        self.created_products.append(created_product['id'])
        
        self.assertEqual(created_product['name'], new_product['name'])
        self.assertEqual(float(created_product['price']), new_product['price'])
        self.assertEqual(created_product['stock'], new_product['stock'])

    def test_03_get_product(self):
        """Test: Récupération d'un produit spécifique"""
        response = requests.get(f"{self.BASE_URL}/products/{self.current_product['id']}/")
        self.assertEqual(response.status_code, 200)
        
        product = response.json()
        self.assertEqual(product['id'], self.current_product['id'])
        self.assertEqual(product['name'], self.current_product['name'])

    def test_04_update_product(self):
        """Test: Mise à jour d'un produit"""
        update_data = {
            "price": 129.99,
            "stock": 45,
            "description": "Description mise à jour pour les tests"
        }
        
        response = requests.put(
            f"{self.BASE_URL}/products/{self.current_product['id']}/",
            json=update_data
        )
        self.assertEqual(response.status_code, 200)
        
        updated_product = response.json()
        self.assertEqual(float(updated_product['price']), update_data['price'])
        self.assertEqual(updated_product['stock'], update_data['stock'])
        self.assertEqual(updated_product['description'], update_data['description'])

    def test_05_delete_product(self):
        """Test: Suppression d'un produit"""
        # Utiliser le produit créé dans setUp
        if hasattr(self, 'current_product'):
            product_id = self.current_product['id']
            
            # Supprimer le produit
            response = requests.delete(f"{self.BASE_URL}/products/{product_id}/")
            self.assertEqual(response.status_code, 204)
            
            # Vérifier que le produit n'existe plus
            response = requests.get(f"{self.BASE_URL}/products/{product_id}/")
            self.assertEqual(response.status_code, 404)
        else:
            self.fail("Pas de produit disponible pour le test")

    def test_06_search_products(self):
        """Test: Recherche de produits"""
        # Utiliser le produit créé dans setUp
        if hasattr(self, 'current_product'):
            # Tester la recherche avec le nom du produit existant
            search_term = self.current_product['name'][:10]  # Utiliser les 10 premiers caractères
            response = requests.post(
                f"{self.BASE_URL}/products/search/",
                json={"search": search_term}
            )
            self.assertEqual(response.status_code, 200)
            results = response.json()
            self.assertIsInstance(results, list)
            self.assertTrue(any(p['id'] == self.current_product['id'] for p in results))
        else:
            self.fail("Pas de produit disponible pour le test")

    def test_07_invalid_product_creation(self):
        """Test: Création d'un produit avec des données invalides"""
        invalid_product = {
            "name": "",  # Nom vide
            "price": -10,  # Prix négatif
            "stock": "invalid",  # Stock non numérique
        }
        
        response = requests.post(f"{self.BASE_URL}/products/", json=invalid_product)
        self.assertEqual(response.status_code, 400)

    def test_08_bulk_operations(self):
        """Test: Opérations en masse"""
        # Créer plusieurs produits
        bulk_products = []
        for i in range(3):
            response = requests.post(f"{self.BASE_URL}/products/", json={
                **self.test_product_data,
                "name": f"Bulk Test Product {i}",
                "slug": f"bulk-test-product-{i}"
            })
            self.assertEqual(response.status_code, 201)
            product = response.json()
            self.created_products.append(product['id'])
            bulk_products.append(product)
        
        # Vérifier que tous les produits ont été créés
        response = requests.get(f"{self.BASE_URL}/products/")
        self.assertEqual(response.status_code, 200)
        all_products = response.json()
        bulk_product_ids = {p['id'] for p in bulk_products}
        found_products = [p for p in all_products if p['id'] in bulk_product_ids]
        self.assertEqual(len(found_products), len(bulk_products))

if __name__ == '__main__':
    unittest.main(verbosity=2)
