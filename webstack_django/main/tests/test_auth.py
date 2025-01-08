import unittest
from unittest.mock import patch, MagicMock
from main.auth.auth_manager import AuthManager
import logging

# Désactiver les logs pendant les tests
logging.disable(logging.CRITICAL)

class TestAuthManager(unittest.TestCase):
    def setUp(self):
        """Configuration initiale pour chaque test"""
        self.auth_manager = AuthManager()
        self.test_user = {
            "email": "test@example.com",
            "password": "Test123!",
            "metadata": {
                "full_name": "Test User",
                "is_admin": False
            }
        }
        self.test_user_id = "test_user_id"

    @patch('main.auth.auth_manager.get_supabase_client')
    def test_sign_up_success(self, mock_get_client):
        """Test d'inscription réussie"""
        # Configuration du mock
        mock_client = MagicMock()
        mock_auth = MagicMock()
        mock_user = MagicMock()
        mock_user.id = self.test_user_id
        mock_user.email = self.test_user["email"]
        mock_response = MagicMock()
        mock_response.user = mock_user
        mock_response.error = None
        mock_auth.sign_up.return_value = mock_response
        mock_client.auth = mock_auth
        mock_get_client.return_value = mock_client

        # Test
        result = self.auth_manager.sign_up(
            self.test_user["email"],
            self.test_user["password"],
            self.test_user["metadata"]
        )

        # Vérifications
        self.assertTrue(result["success"])
        self.assertEqual(result["user"]["id"], self.test_user_id)
        self.assertEqual(result["user"]["email"], self.test_user["email"])
        mock_auth.sign_up.assert_called_once_with({
            "email": self.test_user["email"],
            "password": self.test_user["password"],
            "options": {
                "data": self.test_user["metadata"]
            }
        })

    @patch('main.auth.auth_manager.get_supabase_client')
    def test_sign_in_success(self, mock_get_client):
        """Test de connexion réussie"""
        # Configuration du mock
        mock_client = MagicMock()
        mock_auth = MagicMock()
        mock_user = MagicMock()
        mock_user.id = self.test_user_id
        mock_user.email = self.test_user["email"]
        mock_user.user_metadata = self.test_user["metadata"]
        mock_response = MagicMock()
        mock_response.user = mock_user
        mock_response.error = None
        mock_auth.sign_in_with_password.return_value = mock_response
        mock_client.auth = mock_auth
        mock_get_client.return_value = mock_client

        # Test
        result = self.auth_manager.sign_in(
            self.test_user["email"],
            self.test_user["password"]
        )

        # Vérifications
        self.assertTrue(result["success"])
        self.assertEqual(result["user"]["id"], self.test_user_id)
        self.assertEqual(result["user"]["email"], self.test_user["email"])
        mock_auth.sign_in_with_password.assert_called_once_with({
            "email": self.test_user["email"],
            "password": self.test_user["password"]
        })

    @patch('main.auth.auth_manager.get_supabase_client')
    def test_sign_in_failure(self, mock_get_client):
        """Test d'échec de connexion"""
        # Configuration du mock
        mock_client = MagicMock()
        mock_auth = MagicMock()
        mock_auth.sign_in_with_password.side_effect = Exception("Invalid credentials")
        mock_client.auth = mock_auth
        mock_get_client.return_value = mock_client

        # Test
        result = self.auth_manager.sign_in("wrong@email.com", "wrongpass")

        # Vérifications
        self.assertFalse(result["success"])
        self.assertIn("error", result)
        mock_auth.sign_in_with_password.assert_called_once_with({
            "email": "wrong@email.com",
            "password": "wrongpass"
        })

    @patch('main.auth.auth_manager.get_supabase_client')
    def test_sign_out(self, mock_get_client):
        """Test de déconnexion"""
        # Configuration du mock
        mock_client = MagicMock()
        mock_auth = MagicMock()
        mock_response = MagicMock()
        mock_response.error = None
        mock_auth.sign_out.return_value = mock_response
        mock_client.auth = mock_auth
        mock_get_client.return_value = mock_client

        # Test
        result = self.auth_manager.sign_out()

        # Vérifications
        self.assertTrue(result["success"])
        mock_auth.sign_out.assert_called_once()

    @patch('main.auth.auth_manager.get_supabase_client')
    def test_get_user_success(self, mock_get_client):
        """Test de récupération des informations utilisateur"""
        # Configuration du mock
        mock_client = MagicMock()
        mock_auth = MagicMock()
        mock_user = MagicMock()
        mock_user.id = self.test_user_id
        mock_user.email = self.test_user["email"]
        mock_user.user_metadata = self.test_user["metadata"]
        mock_response = MagicMock()
        mock_response.user = mock_user
        mock_response.error = None
        mock_auth.get_user.return_value = mock_response
        mock_client.auth = mock_auth
        mock_get_client.return_value = mock_client

        # Test
        user = self.auth_manager.get_user()

        # Vérifications
        self.assertIsNotNone(user)
        self.assertEqual(user["id"], self.test_user_id)
        self.assertEqual(user["email"], self.test_user["email"])
        mock_auth.get_user.assert_called_once()

    @patch('main.auth.auth_manager.get_supabase_client')
    def test_is_admin(self, mock_get_client):
        """Test de vérification du statut admin"""
        # Configuration du mock
        mock_client = MagicMock()
        mock_auth = MagicMock()
        mock_user = MagicMock()
        mock_user.id = self.test_user_id
        mock_user.email = self.test_user["email"]
        mock_user.user_metadata = {"is_admin": True}
        mock_response = MagicMock()
        mock_response.user = mock_user
        mock_response.error = None
        mock_auth.get_user.return_value = mock_response
        mock_client.auth = mock_auth
        mock_get_client.return_value = mock_client

        # Test
        is_admin = self.auth_manager.is_admin()

        # Vérifications
        self.assertTrue(is_admin)
        mock_auth.get_user.assert_called_once()

if __name__ == '__main__':
    unittest.main()
