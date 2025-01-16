import unittest
import requests
import json
from dotenv import load_dotenv
import string
import random

# Charger les variables d'environnement
load_dotenv()

class TestValidation(unittest.TestCase):
    """Tests de validation avancés"""
    
    @classmethod
    def setUpClass(cls):
        """Configuration initiale pour tous les tests"""
        cls.BASE_URL = "http://localhost:8000/api"
        cls.valid_category_id = "29bf495e-eb1c-43b1-b753-80a937129628"
    
    def generate_random_string(self, length):
        """Génère une chaîne aléatoire de longueur spécifiée"""
        return ''.join(random.choices(string.ascii_letters + string.digits, k=length))
    
    def test_01_product_name_validation(self):
        """Test: Validation du nom du produit"""
        test_cases = [
            # Trop court
            {"name": "a", "expected_status": 400},
            # Trop long
            {"name": self.generate_random_string(256), "expected_status": 400},
            # Caractères spéciaux
            {"name": "Product@#$%", "expected_status": 400},
            # Vide
            {"name": "", "expected_status": 400},
            # Que des espaces
            {"name": "   ", "expected_status": 400},
            # Valide
            {"name": "Valid Product Name", "expected_status": 201}
        ]
        
        for case in test_cases:
            product_data = {
                "name": case["name"],
                "slug": "test-product",
                "description": "Test product",
                "price": 99.99,
                "stock": 10,
                "category_id": self.valid_category_id
            }
            
            response = requests.post(
                f"{self.BASE_URL}/products/",
                json=product_data
            )
            self.assertEqual(
                response.status_code,
                case["expected_status"],
                f"Failed for name: {case['name']}"
            )
    
    def test_02_price_validation(self):
        """Test: Validation du prix"""
        test_cases = [
            # Prix négatif
            {"price": -10.0, "expected_status": 400},
            # Prix zéro
            {"price": 0, "expected_status": 400},
            # Prix trop élevé
            {"price": 1000000.0, "expected_status": 400},
            # Prix avec trop de décimales
            {"price": 99.999, "expected_status": 400},
            # Prix non numérique
            {"price": "invalid", "expected_status": 400},
            # Prix valide
            {"price": 99.99, "expected_status": 201}
        ]
        
        for case in test_cases:
            product_data = {
                "name": "Test Product",
                "slug": "test-product",
                "description": "Test product",
                "price": case["price"],
                "stock": 10,
                "category_id": self.valid_category_id
            }
            
            response = requests.post(
                f"{self.BASE_URL}/products/",
                json=product_data
            )
            self.assertEqual(
                response.status_code,
                case["expected_status"],
                f"Failed for price: {case['price']}"
            )
    
    def test_03_stock_validation(self):
        """Test: Validation du stock"""
        test_cases = [
            # Stock négatif
            {"stock": -1, "expected_status": 400},
            # Stock non entier
            {"stock": 10.5, "expected_status": 400},
            # Stock trop élevé
            {"stock": 1000000, "expected_status": 400},
            # Stock non numérique
            {"stock": "invalid", "expected_status": 400},
            # Stock valide
            {"stock": 100, "expected_status": 201}
        ]
        
        for case in test_cases:
            product_data = {
                "name": "Test Product",
                "slug": "test-product",
                "description": "Test product",
                "price": 99.99,
                "stock": case["stock"],
                "category_id": self.valid_category_id
            }
            
            response = requests.post(
                f"{self.BASE_URL}/products/",
                json=product_data
            )
            self.assertEqual(
                response.status_code,
                case["expected_status"],
                f"Failed for stock: {case['stock']}"
            )
    
    def test_04_slug_validation(self):
        """Test: Validation du slug"""
        test_cases = [
            # Slug avec espaces
            {"slug": "test product", "expected_status": 400},
            # Slug avec caractères spéciaux
            {"slug": "test@product", "expected_status": 400},
            # Slug trop long
            {"slug": "test-" + self.generate_random_string(100), "expected_status": 400},
            # Slug vide
            {"slug": "", "expected_status": 400},
            # Slug valide
            {"slug": "valid-product-slug", "expected_status": 201}
        ]
        
        for case in test_cases:
            product_data = {
                "name": "Test Product",
                "slug": case["slug"],
                "description": "Test product",
                "price": 99.99,
                "stock": 10,
                "category_id": self.valid_category_id
            }
            
            response = requests.post(
                f"{self.BASE_URL}/products/",
                json=product_data
            )
            self.assertEqual(
                response.status_code,
                case["expected_status"],
                f"Failed for slug: {case['slug']}"
            )
    
    def test_05_unique_constraints(self):
        """Test: Contraintes d'unicité"""
        # Créer un premier produit
        product_data = {
            "name": "Unique Test Product",
            "slug": "unique-test-product",
            "description": "Test product",
            "price": 99.99,
            "stock": 10,
            "category_id": self.valid_category_id
        }
        
        response = requests.post(
            f"{self.BASE_URL}/products/",
            json=product_data
        )
        self.assertEqual(response.status_code, 201)
        
        # Tenter de créer un produit avec le même slug
        response = requests.post(
            f"{self.BASE_URL}/products/",
            json=product_data
        )
        self.assertEqual(response.status_code, 400)

if __name__ == '__main__':
    unittest.main(verbosity=2)
