import unittest
from unittest.mock import patch, MagicMock
from main.products.product_manager import ProductManager
import logging

# Désactiver les logs pendant les tests
logging.disable(logging.CRITICAL)

class TestProductManager(unittest.TestCase):
    def setUp(self):
        """Configuration initiale pour chaque test"""
        self.product_manager = ProductManager()
        self.test_product_data = {
            "name": "Test Product",
            "description": "A test product",
            "price": 99.99,
            "stock": 10,
            "category_id": "test_category_id",
            "brand_id": "test_brand_id",
            "is_active": True
        }
        self.test_product_id = "test_product_id"

    @patch('main.products.product_manager.get_supabase_client')
    def test_create_product_success(self, mock_get_client):
        """Test de création de produit réussie"""
        # Configuration du mock
        mock_client = MagicMock()
        mock_response = MagicMock()
        mock_response.data = [{
            **self.test_product_data,
            "id": self.test_product_id,
            "slug": "test-product"
        }]
        mock_response.error = None
        
        # Configuration de la chaîne de méthodes
        mock_query = MagicMock()
        mock_query.insert.return_value = mock_query
        mock_query.execute.return_value = mock_response
        
        mock_client.table.return_value = mock_query
        mock_get_client.return_value = mock_client

        # Test
        result = self.product_manager.create_product(self.test_product_data)

        # Vérifications
        self.assertTrue(result["success"])
        self.assertEqual(result["data"]["name"], self.test_product_data["name"])
        self.assertEqual(result["data"]["slug"], "test-product")
        mock_client.table.assert_called_once_with("products")
        mock_query.insert.assert_called_once_with({**self.test_product_data, "slug": "test-product"})
        mock_query.execute.assert_called_once()

    @patch('main.products.product_manager.get_supabase_client')
    def test_get_product_by_id_success(self, mock_get_client):
        """Test de récupération d'un produit par ID"""
        # Configuration du mock
        mock_client = MagicMock()
        mock_response = MagicMock()
        mock_response.data = {
            **self.test_product_data,
            "id": self.test_product_id,
            "slug": "test-product",
            "category": {"id": "test_category_id", "name": "Test Category"},
            "brand": {"id": "test_brand_id", "name": "Test Brand"}
        }
        mock_response.error = None
        
        # Configuration de la chaîne de méthodes
        mock_query = MagicMock()
        mock_query.select.return_value = mock_query
        mock_query.eq.return_value = mock_query
        mock_query.single.return_value = mock_query
        mock_query.execute.return_value = mock_response
        
        mock_client.table.return_value = mock_query
        mock_get_client.return_value = mock_client

        # Test
        result = self.product_manager.get_product_by_id(self.test_product_id)

        # Vérifications
        self.assertTrue(result["success"])
        self.assertEqual(result["data"]["id"], self.test_product_id)
        self.assertEqual(result["data"]["category"]["name"], "Test Category")
        self.assertEqual(result["data"]["brand"]["name"], "Test Brand")
        mock_client.table.assert_called_once_with("products")
        mock_query.select.assert_called_once_with("*, category:categories(*), brand:brands(*)")
        mock_query.eq.assert_called_once_with("id", self.test_product_id)
        mock_query.single.assert_called_once()
        mock_query.execute.assert_called_once()

    @patch('main.products.product_manager.get_supabase_client')
    def test_get_products_with_filters(self, mock_get_client):
        """Test de récupération des produits avec filtres"""
        # Configuration du mock
        mock_client = MagicMock()
        mock_response = MagicMock()
        mock_response.data = [{
            **self.test_product_data,
            "id": self.test_product_id,
            "slug": "test-product",
            "category": {"id": "test_category_id", "name": "Test Category"},
            "brand": {"id": "test_brand_id", "name": "Test Brand"}
        }]
        mock_response.error = None
        
        # Configuration de la chaîne de méthodes
        mock_query = MagicMock()
        mock_query.select.return_value = mock_query
        mock_query.eq.return_value = mock_query
        mock_query.gte.return_value = mock_query
        mock_query.lte.return_value = mock_query
        mock_query.order.return_value = mock_query
        mock_query.range.return_value = mock_query
        mock_query.execute.return_value = mock_response
        
        mock_client.table.return_value = mock_query
        mock_get_client.return_value = mock_client

        # Test
        result = self.product_manager.get_products(
            limit=10,
            category_id="test_category_id",
            min_price=50,
            max_price=100,
            sort_by="price_asc"
        )

        # Vérifications
        self.assertTrue(result["success"])
        self.assertEqual(len(result["data"]), 1)
        self.assertEqual(result["data"][0]["price"], 99.99)
        mock_client.table.assert_called_once_with("products")
        mock_query.select.assert_called_once_with("*, category:categories(*), brand:brands(*)")
        mock_query.execute.assert_called_once()

    @patch('main.products.product_manager.get_supabase_client')
    def test_update_product_success(self, mock_get_client):
        """Test de mise à jour d'un produit"""
        # Configuration du mock
        mock_client = MagicMock()
        mock_response = MagicMock()
        update_data = {"price": 89.99, "description": "Updated description"}
        mock_response.data = [{
            **self.test_product_data,
            **update_data,
            "id": self.test_product_id
        }]
        mock_response.error = None
        
        # Configuration de la chaîne de méthodes
        mock_query = MagicMock()
        mock_query.update.return_value = mock_query
        mock_query.eq.return_value = mock_query
        mock_query.execute.return_value = mock_response
        
        mock_client.table.return_value = mock_query
        mock_get_client.return_value = mock_client

        # Test
        result = self.product_manager.update_product(self.test_product_id, update_data)

        # Vérifications
        self.assertTrue(result["success"])
        self.assertEqual(result["data"]["price"], 89.99)
        self.assertEqual(result["data"]["description"], "Updated description")
        mock_client.table.assert_called_once_with("products")
        mock_query.update.assert_called_once_with(update_data)
        mock_query.eq.assert_called_once_with("id", self.test_product_id)
        mock_query.execute.assert_called_once()

    @patch('main.products.product_manager.get_supabase_client')
    def test_delete_product_success(self, mock_get_client):
        """Test de suppression douce d'un produit"""
        # Configuration du mock
        mock_client = MagicMock()
        mock_response = MagicMock()
        mock_response.data = [{
            **self.test_product_data,
            "id": self.test_product_id,
            "is_active": False
        }]
        mock_response.error = None
        
        # Configuration de la chaîne de méthodes
        mock_query = MagicMock()
        mock_query.update.return_value = mock_query
        mock_query.eq.return_value = mock_query
        mock_query.execute.return_value = mock_response
        
        mock_client.table.return_value = mock_query
        mock_get_client.return_value = mock_client

        # Test
        result = self.product_manager.delete_product(self.test_product_id)

        # Vérifications
        self.assertTrue(result["success"])
        self.assertFalse(result["data"]["is_active"])
        mock_client.table.assert_called_once_with("products")
        mock_query.update.assert_called_once_with({"is_active": False})
        mock_query.eq.assert_called_once_with("id", self.test_product_id)
        mock_query.execute.assert_called_once()

if __name__ == '__main__':
    unittest.main()
