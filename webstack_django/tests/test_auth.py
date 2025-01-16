import unittest
import requests
import json
import os
from dotenv import load_dotenv
import jwt
import time
from datetime import datetime, timedelta

# Charger les variables d'environnement
load_dotenv()

class TestAuthentication(unittest.TestCase):
    """Tests d'authentification et d'autorisation"""
    
    @classmethod
    def setUpClass(cls):
        """Configuration initiale pour tous les tests"""
        cls.BASE_URL = "http://localhost:8000/api"
        cls.SUPABASE_URL = os.getenv('SUPABASE_URL')
        cls.SUPABASE_ANON_KEY = os.getenv('SUPABASE_ANON_KEY')
        cls.SUPABASE_SERVICE_KEY = os.getenv('SUPABASE_SERVICE_KEY')
        
        # Créer un token valide pour les tests
        cls.valid_token = jwt.encode({
            'sub': 'test_user',
            'email': 'test@example.com',
            'role': 'user',
            'exp': datetime.now() + timedelta(hours=1)
        }, 'secret', algorithm='HS256')
        
        # Créer un token admin valide
        cls.admin_token = jwt.encode({
            'sub': 'admin_user',
            'email': 'admin@example.com',
            'role': 'admin',
            'exp': datetime.now() + timedelta(hours=1)
        }, 'secret', algorithm='HS256')
        
    def setUp(self):
        """Configuration avant chaque test"""
        self.headers = {
            "Content-Type": "application/json"
        }
        
        # Données de test pour un produit
        self.test_product = {
            "name": "Test Product",
            "slug": f"test-product-{int(time.time())}",
            "description": "A test product",
            "price": 99.99,
            "stock": 10,
            "category_id": "29bf495e-eb1c-43b1-b753-80a937129628"
        }
    
    def test_01_anonymous_access(self):
        """Test: Accès anonyme aux endpoints publics"""
        # Test accès à la liste des produits sans authentification
        response = requests.get(f"{self.BASE_URL}/products/")
        self.assertEqual(response.status_code, 200)
        
        # Test accès à un produit spécifique sans authentification
        products = response.json()
        if products:
            product_id = products[0]['id']
            response = requests.get(f"{self.BASE_URL}/products/{product_id}/")
            self.assertEqual(response.status_code, 200)
    
    def test_02_protected_endpoints(self):
        """Test: Accès aux endpoints protégés"""
        # Test création de produit sans authentification
        response = requests.post(
            f"{self.BASE_URL}/products/",
            json=self.test_product,
            headers=self.headers
        )
        self.assertEqual(response.status_code, 401)
        
        # Test avec authentification valide
        self.headers["Authorization"] = f"Bearer {self.valid_token}"
        response = requests.post(
            f"{self.BASE_URL}/products/",
            json=self.test_product,
            headers=self.headers
        )
        self.assertEqual(response.status_code, 201)
    
    def test_03_invalid_token(self):
        """Test: Tentative d'accès avec un token invalide"""
        self.headers["Authorization"] = "Bearer invalid_token"
        response = requests.post(
            f"{self.BASE_URL}/products/",
            json=self.test_product,
            headers=self.headers
        )
        self.assertEqual(response.status_code, 401)
    
    def test_04_expired_token(self):
        """Test: Tentative d'accès avec un token expiré"""
        # Créer un token JWT expiré
        expired_token = jwt.encode({
            'sub': 'test_user',
            'exp': int(time.time()) - 3600  # Token expiré il y a 1 heure
        }, 'secret', algorithm='HS256')
        
        self.headers["Authorization"] = f"Bearer {expired_token}"
        response = requests.post(
            f"{self.BASE_URL}/products/",
            json=self.test_product,
            headers=self.headers
        )
        self.assertEqual(response.status_code, 401)
    
    def test_05_role_based_access(self):
        """Test: Accès basé sur les rôles"""
        # Créer un produit avec un utilisateur normal
        self.headers["Authorization"] = f"Bearer {self.valid_token}"
        response = requests.post(
            f"{self.BASE_URL}/products/",
            json=self.test_product,
            headers=self.headers
        )
        self.assertEqual(response.status_code, 201)
        product_id = response.json()['id']
        
        # Tenter de supprimer le produit avec un utilisateur normal
        response = requests.delete(
            f"{self.BASE_URL}/products/{product_id}/",
            headers=self.headers
        )
        self.assertEqual(response.status_code, 403)  # Forbidden pour les non-admins
        
        # Supprimer le produit avec un admin
        self.headers["Authorization"] = f"Bearer {self.admin_token}"
        response = requests.delete(
            f"{self.BASE_URL}/products/{product_id}/",
            headers=self.headers
        )
        self.assertEqual(response.status_code, 204)  # Succès pour l'admin
    
    def test_06_rate_limiting(self):
        """Test: Limitation du taux de requêtes"""
        # Faire plusieurs requêtes rapidement
        for _ in range(50):
            response = requests.get(f"{self.BASE_URL}/products/")
            if response.status_code == 429:  # Rate limit atteint
                break
        
        self.assertIn(response.status_code, [200, 429])

if __name__ == '__main__':
    unittest.main(verbosity=2)
