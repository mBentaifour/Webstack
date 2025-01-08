from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from unittest.mock import patch
from main.supabase_adapter import SupabaseAdapter

User = get_user_model()

class StockAlertsTests(TestCase):
    def setUp(self):
        # Créer un utilisateur admin
        self.admin_user = User.objects.create_superuser(
            username='admin',
            email='admin@test.com',
            password='testpass123'
        )
        
        # Créer un utilisateur normal
        self.normal_user = User.objects.create_user(
            username='user',
            email='user@test.com',
            password='testpass123'
        )
        
        self.client = Client()
        
        # Mock data pour les alertes
        self.mock_alert = {
            'id': 'test-alert-id',
            'product_id': 'test-product-id',
            'type': 'low_stock',
            'message': 'Stock bas pour Test Product',
            'current_stock': 5,
            'threshold': 10,
            'status': 'pending',
            'created_at': '2024-01-01T00:00:00',
            'products': {'name': 'Test Product'}
        }

    def test_stock_alerts_view_admin_access(self):
        """Test que seuls les admins peuvent accéder à la vue des alertes."""
        self.client.login(username='admin', password='testpass123')
        
        with patch.object(SupabaseAdapter, 'get_stock_alerts') as mock_get:
            mock_get.return_value = {'success': True, 'data': [self.mock_alert]}
            response = self.client.get(reverse('main:stock_alerts'))
            
            self.assertEqual(response.status_code, 200)
            self.assertTemplateUsed(response, 'main/stock_alerts.html')
            self.assertContains(response, 'Test Product')

    def test_stock_alerts_view_user_access_denied(self):
        """Test que les utilisateurs normaux ne peuvent pas accéder aux alertes."""
        self.client.login(username='user', password='testpass123')
        
        response = self.client.get(reverse('main:stock_alerts'))
        self.assertEqual(response.status_code, 302)  # Redirection
        self.assertRedirects(response, reverse('main:home'))

    def test_process_stock_alert_success(self):
        """Test le traitement réussi d'une alerte."""
        self.client.login(username='admin', password='testpass123')
        
        with patch.object(SupabaseAdapter, 'update_stock_alert_status') as mock_update:
            mock_update.return_value = {'success': True, 'data': self.mock_alert}
            
            response = self.client.post(
                reverse('main:process_stock_alert', args=['test-alert-id']),
                {'action': 'process'}
            )
            
            self.assertEqual(response.status_code, 302)
            self.assertRedirects(response, reverse('main:stock_alerts'))
            mock_update.assert_called_once()

    def test_check_stock_levels_success(self):
        """Test la vérification manuelle des niveaux de stock."""
        self.client.login(username='admin', password='testpass123')
        
        with patch.object(SupabaseAdapter, 'check_stock_levels') as mock_check:
            mock_check.return_value = {
                'success': True,
                'data': {'alerts_created': 2, 'alerts': []}
            }
            
            response = self.client.post(reverse('main:check_stock_levels'))
            
            self.assertEqual(response.status_code, 302)
            self.assertRedirects(response, reverse('main:stock_alerts'))
            mock_check.assert_called_once()

    def test_invalid_alert_action(self):
        """Test qu'une action invalide est rejetée."""
        self.client.login(username='admin', password='testpass123')
        
        response = self.client.post(
            reverse('main:process_stock_alert', args=['test-alert-id']),
            {'action': 'invalid_action'}
        )
        
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('main:stock_alerts'))

    def test_get_stock_alerts_with_filter(self):
        """Test le filtrage des alertes par statut."""
        self.client.login(username='admin', password='testpass123')
        
        with patch.object(SupabaseAdapter, 'get_stock_alerts') as mock_get:
            mock_get.return_value = {'success': True, 'data': [self.mock_alert]}
            
            response = self.client.get(
                reverse('main:stock_alerts'),
                {'status': 'pending'}
            )
            
            self.assertEqual(response.status_code, 200)
            mock_get.assert_called_with(status='pending')

    def test_stock_alerts_api_error(self):
        """Test la gestion des erreurs de l'API."""
        self.client.login(username='admin', password='testpass123')
        
        with patch.object(SupabaseAdapter, 'get_stock_alerts') as mock_get:
            mock_get.return_value = {
                'success': False,
                'error': "Erreur de l'API"
            }
            
            response = self.client.get(reverse('main:stock_alerts'))
            
            self.assertEqual(response.status_code, 302)
            self.assertRedirects(response, reverse('main:dashboard'))

    def test_check_stock_levels_api_error(self):
        """Test la gestion des erreurs lors de la vérification des stocks."""
        self.client.login(username='admin', password='testpass123')
        
        with patch.object(SupabaseAdapter, 'check_stock_levels') as mock_check:
            mock_check.return_value = {
                'success': False,
                'error': "Erreur de l'API"
            }
            
            response = self.client.post(reverse('main:check_stock_levels'))
            
            self.assertEqual(response.status_code, 302)
            self.assertRedirects(response, reverse('main:stock_alerts'))

import unittest
from unittest.mock import patch, MagicMock
from main.stock.stock_alert_manager import StockAlertManager
import logging

logging.disable(logging.CRITICAL)

class TestStockAlertManager(unittest.TestCase):
    def setUp(self):
        self.stock_alert_manager = StockAlertManager()
        self.test_alert_data = {
            "product_id": "test_product_id",
            "threshold": 5,
            "user_id": "test_user_id",
            "is_active": True
        }
        self.test_alert_id = "test_alert_id"

    @patch('main.stock.stock_alert_manager.get_supabase_client')
    def test_create_stock_alert(self, mock_get_client):
        """Test la création d'une alerte de stock"""
        mock_client = MagicMock()
        mock_response = MagicMock()
        mock_response.data = [{"id": self.test_alert_id, **self.test_alert_data}]
        mock_response.error = None
        
        mock_query = MagicMock()
        mock_query.insert.return_value = mock_query
        mock_query.execute.return_value = mock_response
        
        mock_client.table.return_value = mock_query
        mock_get_client.return_value = mock_client

        result = self.stock_alert_manager.create_alert(self.test_alert_data)

        self.assertTrue(result["success"])
        self.assertEqual(result["data"]["id"], self.test_alert_id)
        mock_client.table.assert_called_once_with("stock_alerts")

    @patch('main.stock.stock_alert_manager.get_supabase_client')
    def test_get_active_alerts(self, mock_get_client):
        """Test la récupération des alertes actives"""
        mock_client = MagicMock()
        mock_response = MagicMock()
        mock_response.data = [{"id": self.test_alert_id, **self.test_alert_data}]
        mock_response.error = None
        
        mock_query = MagicMock()
        mock_query.select.return_value = mock_query
        mock_query.eq.return_value = mock_query
        mock_query.execute.return_value = mock_response
        
        mock_client.table.return_value = mock_query
        mock_get_client.return_value = mock_client

        result = self.stock_alert_manager.get_active_alerts()

        self.assertTrue(result["success"])
        self.assertEqual(len(result["data"]), 1)
        mock_client.table.assert_called_once_with("stock_alerts")

    @patch('main.stock.stock_alert_manager.get_supabase_client')
    def test_process_alerts(self, mock_get_client):
        """Test le traitement des alertes de stock"""
        mock_client = MagicMock()
        mock_response = MagicMock()
        mock_response.data = [{
            "id": self.test_alert_id,
            **self.test_alert_data,
            "product": {
                "id": "test_product_id",
                "name": "Test Product",
                "stock": 3
            }
        }]
        mock_response.error = None
        
        mock_query = MagicMock()
        mock_query.select.return_value = mock_query
        mock_query.eq.return_value = mock_query
        mock_query.execute.return_value = mock_response
        
        mock_client.table.return_value = mock_query
        mock_get_client.return_value = mock_client

        result = self.stock_alert_manager.process_alerts()

        self.assertTrue(result["success"])
        self.assertTrue(len(result["processed_alerts"]) > 0)
        mock_client.table.assert_called_with("stock_alerts")

if __name__ == '__main__':
    unittest.main()
