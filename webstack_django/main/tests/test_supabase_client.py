import unittest
from unittest.mock import patch, MagicMock
from main.supabase.client import get_supabase_client, reset_supabase_client
import os
import logging

# Désactiver les logs pendant les tests
logging.disable(logging.CRITICAL)

class TestSupabaseClient(unittest.TestCase):
    def setUp(self):
        """Configuration initiale pour chaque test"""
        # Réinitialiser le client avant chaque test
        reset_supabase_client()
        
        # Sauvegarder les variables d'environnement originales
        self.original_env = {}
        for key in ['SUPABASE_URL', 'SUPABASE_KEY']:
            self.original_env[key] = os.environ.get(key)
            if key in os.environ:
                del os.environ[key]

    def tearDown(self):
        """Nettoyage après chaque test"""
        # Restaurer les variables d'environnement originales
        for key, value in self.original_env.items():
            if value is not None:
                os.environ[key] = value
            elif key in os.environ:
                del os.environ[key]
        
        # Réinitialiser le client
        reset_supabase_client()

    @patch('main.supabase.client.create_client')
    def test_get_supabase_client_singleton(self, mock_create_client):
        """Test que get_supabase_client retourne la même instance"""
        # Configurer les variables d'environnement pour le test
        os.environ['SUPABASE_URL'] = 'https://test.supabase.co'
        os.environ['SUPABASE_KEY'] = 'test-key'
        
        # Configuration du mock
        mock_client = MagicMock()
        mock_create_client.return_value = mock_client

        # Premier appel
        client1 = get_supabase_client()
        # Deuxième appel
        client2 = get_supabase_client()

        # Vérifications
        self.assertEqual(client1, client2)
        # create_client ne devrait être appelé qu'une seule fois
        mock_create_client.assert_called_once()

    @patch('main.supabase.client.create_client')
    def test_reset_supabase_client(self, mock_create_client):
        """Test que reset_supabase_client réinitialise bien le client"""
        # Configurer les variables d'environnement pour le test
        os.environ['SUPABASE_URL'] = 'https://test.supabase.co'
        os.environ['SUPABASE_KEY'] = 'test-key'
        
        # Configuration du mock
        mock_client1 = MagicMock()
        mock_client2 = MagicMock()
        mock_create_client.side_effect = [mock_client1, mock_client2]

        # Premier appel
        client1 = get_supabase_client()
        # Réinitialisation
        reset_supabase_client()
        # Deuxième appel
        client2 = get_supabase_client()

        # Vérifications
        self.assertNotEqual(client1, client2)
        self.assertEqual(mock_create_client.call_count, 2)

    @patch('main.supabase.client.load_dotenv')
    @patch('main.supabase.client.os.getenv')
    def test_get_supabase_client_missing_env(self, mock_getenv, mock_load_dotenv):
        """Test que get_supabase_client lève une erreur si les variables d'environnement sont manquantes"""
        # Configuration des mocks
        mock_load_dotenv.return_value = None
        mock_getenv.return_value = None
        
        # Vérifier que l'exception est levée
        with self.assertRaises(ValueError) as context:
            get_supabase_client()

        self.assertIn("Les variables d'environnement SUPABASE_URL et SUPABASE_KEY sont requises", 
                     str(context.exception))

if __name__ == '__main__':
    unittest.main()
