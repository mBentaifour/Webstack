import os
import requests
import logging
from dotenv import load_dotenv
from main.supabase_adapter import SupabaseAdapter
from main.auth_manager import AuthManager

# Configuration du logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SystemTester:
    def __init__(self):
        # Charger les variables d'environnement de test
        load_dotenv('.env.test')
        
        self.base_url = "http://localhost:8000"
        self.auth_manager = AuthManager()
        self.supabase_adapter = SupabaseAdapter()
        self.access_token = None
        
        # Vérifier que les variables d'environnement sont présentes
        required_vars = ['TEST_USER_EMAIL', 'TEST_USER_PASSWORD', 'SUPABASE_URL', 'SUPABASE_KEY']
        missing_vars = [var for var in required_vars if not os.getenv(var)]
        
        if missing_vars:
            raise ValueError(f"Variables d'environnement manquantes: {', '.join(missing_vars)}")
            
    def run_all_tests(self):
        """Exécute tous les tests du système"""
        try:
            logger.info("=== Début des tests système ===")
            
            # Test 1: Authentification
            self.test_authentication()
            
            # Test 2: Gestion des produits
            self.test_products()
            
            # Test 3: Gestion des notifications
            self.test_notifications()
            
            # Test 4: Sécurité
            self.test_security()
            
            logger.info("=== Tous les tests sont terminés avec succès ===")
            
        except Exception as e:
            logger.error(f"Erreur lors des tests: {str(e)}")
            raise

    def test_authentication(self):
        """Test du système d'authentification"""
        logger.info("Test d'authentification...")
        
        # Test de connexion
        email = os.getenv("TEST_USER_EMAIL", "test@example.com")
        password = os.getenv("TEST_USER_PASSWORD", "testpassword")
        
        result = self.auth_manager.login(email, password)
        assert result["success"], "Échec de la connexion"
        
        # Extraire le token de la session
        session_data = result.get("data", {})
        if isinstance(session_data, dict):
            self.access_token = session_data.get("session", {}).get("access_token")
        else:
            self.access_token = getattr(session_data, "session", {}).get("access_token")
            
        assert self.access_token, "Token d'accès non trouvé"
        logger.info("✅ Test de connexion réussi")
        
        # Test de rafraîchissement de session
        headers = {"Authorization": f"Bearer {self.access_token}"}
        response = requests.get(f"{self.base_url}/api/profile/", headers=headers)
        assert response.status_code == 200, "Échec de l'accès au profil"
        logger.info("✅ Test d'accès au profil réussi")

    def test_products(self):
        """Test du système de gestion des produits"""
        logger.info("Test de gestion des produits...")
        
        # Test de récupération des produits
        headers = {"Authorization": f"Bearer {self.access_token}"}
        
        # Liste des produits
        response = requests.get(f"{self.base_url}/api/products/", headers=headers)
        assert response.status_code == 200, "Échec de récupération des produits"
        products = response.json()
        logger.info(f"✅ {len(products)} produits récupérés")
        
        # Test des catégories
        response = requests.get(f"{self.base_url}/api/categories/", headers=headers)
        assert response.status_code == 200, "Échec de récupération des catégories"
        categories = response.json()
        logger.info(f"✅ {len(categories)} catégories récupérées")

    def test_notifications(self):
        """Test du système de notifications"""
        logger.info("Test des notifications...")
        
        if not self.access_token:
            logger.error("Token d'accès non disponible")
            return
            
        headers = {"Authorization": f"Bearer {self.access_token}"}
        
        # Créer une notification de test
        notification_data = {
            "title": "Test Notification",
            "message": "Ceci est un test",
            "type": "info"
        }
        
        response = requests.post(
            f"{self.base_url}/api/notifications/create/",
            headers=headers,
            json=notification_data
        )
        assert response.status_code == 201, "Échec de création de notification"
        logger.info("✅ Création de notification réussie")
        
        # Récupérer les notifications
        response = requests.get(f"{self.base_url}/api/notifications/", headers=headers)
        assert response.status_code == 200, "Échec de récupération des notifications"
        notifications = response.json()
        logger.info(f"✅ {len(notifications)} notifications récupérées")

    def test_security(self):
        """Test des fonctionnalités de sécurité"""
        logger.info("Test de sécurité...")
        
        # Test des en-têtes de sécurité
        response = requests.get(f"{self.base_url}/")
        headers = response.headers
        
        security_headers = [
            'X-Frame-Options',
            'X-Content-Type-Options',
            'X-XSS-Protection',
            'Strict-Transport-Security',
            'Referrer-Policy'
        ]
        
        for header in security_headers:
            assert header in headers, f"En-tête {header} manquant"
        logger.info("✅ En-têtes de sécurité présents")
        
        # Test du rate limiting
        for _ in range(70):  # Dépasse la limite de 60 requêtes/minute
            response = requests.get(f"{self.base_url}/")
        
        response = requests.get(f"{self.base_url}/")
        assert response.status_code == 429, "Le rate limiting ne fonctionne pas"
        logger.info("✅ Rate limiting fonctionne correctement")

if __name__ == "__main__":
    tester = SystemTester()
    tester.run_all_tests()
