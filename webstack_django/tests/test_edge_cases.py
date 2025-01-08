import unittest
import requests
import json
from dotenv import load_dotenv
import string
import random

# Charger les variables d'environnement
load_dotenv()

class TestEdgeCases(unittest.TestCase):
    """Tests des cas limites et situations exceptionnelles"""
    
    @classmethod
    def setUpClass(cls):
        """Configuration initiale pour tous les tests"""
        cls.BASE_URL = "http://localhost:8000/api"
        cls.valid_category_id = "29bf495e-eb1c-43b1-b753-80a937129628"
    
    def test_01_malformed_json(self):
        """Test: Envoi de JSON malformé"""
        headers = {"Content-Type": "application/json"}
        
        # JSON invalide
        response = requests.post(
            f"{self.BASE_URL}/products/",
            data="{invalid_json",
            headers=headers
        )
        self.assertEqual(response.status_code, 400)
        
        # JSON vide
        response = requests.post(
            f"{self.BASE_URL}/products/",
            data="{}",
            headers=headers
        )
        self.assertEqual(response.status_code, 400)
        
        # Array au lieu d'objet
        response = requests.post(
            f"{self.BASE_URL}/products/",
            data="[]",
            headers=headers
        )
        self.assertEqual(response.status_code, 400)
    
    def test_02_unicode_handling(self):
        """Test: Gestion des caractères Unicode"""
        test_cases = [
            # Emojis
            {"name": "Test Product 🎉", "expected_status": 201},
            # Caractères chinois
            {"name": "测试产品", "expected_status": 201},
            # Caractères arabes
            {"name": "منتج اختبار", "expected_status": 201},
            # Caractères spéciaux
            {"name": "Produit™ de test №1", "expected_status": 201}
        ]
        
        for case in test_cases:
            product_data = {
                "name": case["name"],
                "slug": f"test-product-{random.randint(1000, 9999)}",
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
    
    def test_03_boundary_values(self):
        """Test: Valeurs limites"""
        test_cases = [
            # Prix maximum possible
            {
                "price": 999999.99,
                "stock": 100,
                "expected_status": 201
            },
            # Stock maximum
            {
                "price": 99.99,
                "stock": 999999,
                "expected_status": 201
            },
            # Description très longue
            {
                "description": "x" * 9999,
                "expected_status": 400
            }
        ]
        
        for case in test_cases:
            product_data = {
                "name": "Test Product",
                "slug": f"test-product-{random.randint(1000, 9999)}",
                "description": case.get("description", "Test product"),
                "price": case["price"],
                "stock": case["stock"],
                "category_id": self.valid_category_id
            }
            
            response = requests.post(
                f"{self.BASE_URL}/products/",
                json=product_data
            )
            self.assertEqual(response.status_code, case["expected_status"])
    
    def test_04_concurrent_modifications(self):
        """Test: Modifications concurrentes"""
        # Créer un produit pour le test
        product_data = {
            "name": "Concurrent Test Product",
            "slug": "concurrent-test-product",
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
        product_id = response.json()['id']
        
        # Tenter de modifier le même produit simultanément
        update_data_1 = {"price": 199.99}
        update_data_2 = {"price": 299.99}
        
        response1 = requests.put(
            f"{self.BASE_URL}/products/{product_id}/",
            json=update_data_1
        )
        response2 = requests.put(
            f"{self.BASE_URL}/products/{product_id}/",
            json=update_data_2
        )
        
        self.assertTrue(
            response1.status_code in [200, 409] and
            response2.status_code in [200, 409]
        )
    
    def test_05_special_characters_in_urls(self):
        """Test: Caractères spéciaux dans les URLs"""
        special_chars = ['#', '?', '&', '=', '+', '%20', '@']
        
        for char in special_chars:
            response = requests.get(f"{self.BASE_URL}/products/invalid{char}id/")
            self.assertEqual(response.status_code, 404)
    
    def test_06_large_batch_operations(self):
        """Test: Opérations par lots de grande taille"""
        # Créer une grande liste de produits
        products = []
        for i in range(100):
            products.append({
                "name": f"Bulk Product {i}",
                "slug": f"bulk-product-{i}",
                "description": "Bulk test product",
                "price": 99.99,
                "stock": 10,
                "category_id": self.valid_category_id
            })
        
        # Tester l'envoi en masse
        response = requests.post(
            f"{self.BASE_URL}/products/bulk/",
            json={"products": products}
        )
        self.assertTrue(response.status_code in [201, 413])  # 413 si trop grand
    
    def test_07_network_timeouts(self):
        """Test: Timeouts réseau"""
        # Simuler une requête lente
        response = requests.get(
            f"{self.BASE_URL}/products/",
            timeout=0.001  # Timeout très court
        )
        self.assertTrue(response.status_code in [200, 408, 504])

if __name__ == '__main__':
    unittest.main(verbosity=2)
