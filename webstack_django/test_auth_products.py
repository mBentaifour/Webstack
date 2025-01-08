import os
from dotenv import load_dotenv
import logging
from main.supabase_config import get_supabase_client, get_supabase_admin_client
import random
import string

# Configuration du logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Charger les variables d'environnement
load_dotenv()

def generate_test_user():
    """Génère des données de test pour un utilisateur"""
    random_string = ''.join(random.choices(string.ascii_lowercase, k=8))
    return {
        'email': f'{random_string}@gmail.com',  # Utilisation d'un domaine email valide
        'password': 'TestPassword123!',
        'username': f'testuser_{random_string}'
    }

def test_auth():
    """Teste l'authentification"""
    try:
        client = get_supabase_client()
        
        # Utiliser un compte de test existant
        test_credentials = {
            'email': os.getenv('ADMIN_EMAIL'),
            'password': os.getenv('ADMIN_PASSWORD')
        }
        
        # Test de connexion avec un compte existant
        logger.info("Test de connexion...")
        signin_response = client.auth.sign_in_with_password({
            "email": test_credentials['email'],
            "password": test_credentials['password']
        })
        logger.info("✅ Connexion réussie")
        
        # Stocker le token pour les tests suivants
        access_token = signin_response.session.access_token
        logger.info("✅ Token d'accès récupéré")
        
        return access_token, test_credentials
        
    except Exception as e:
        logger.error(f"❌ Erreur lors des tests d'authentification: {str(e)}")
        return None, None

def test_product_operations(access_token):
    """Teste les opérations CRUD sur les produits"""
    try:
        # Utiliser le client admin pour les opérations sensibles
        admin_client = get_supabase_admin_client()
        
        # 1. Test de création d'un produit
        logger.info("Test de création d'un produit...")
        test_product = {
            'name': 'Produit Test',
            'description': 'Description du produit test',
            'price': 19.99,
            'stock': 100,
            'category_id': 1,  # Assurez-vous que cette catégorie existe
            'brand_id': 1      # Assurez-vous que cette marque existe
        }
        
        insert_response = admin_client.table('products').insert(test_product).execute()
        product_id = insert_response.data[0]['id']
        logger.info(f"✅ Produit créé avec l'ID: {product_id}")
        
        # 2. Test de lecture d'un produit
        logger.info("Test de lecture d'un produit...")
        read_response = admin_client.table('products').select('*').eq('id', product_id).execute()
        assert len(read_response.data) > 0, "Le produit n'a pas été trouvé"
        logger.info("✅ Lecture du produit réussie")
        
        # 3. Test de mise à jour d'un produit
        logger.info("Test de mise à jour d'un produit...")
        update_data = {'name': 'Produit Test Modifié'}
        update_response = admin_client.table('products').update(update_data).eq('id', product_id).execute()
        logger.info("✅ Mise à jour du produit réussie")
        
        # 4. Test de suppression d'un produit
        logger.info("Test de suppression d'un produit...")
        delete_response = admin_client.table('products').delete().eq('id', product_id).execute()
        logger.info("✅ Suppression du produit réussie")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Erreur lors des tests des produits: {str(e)}")
        return False

def cleanup_test_user(test_user):
    """Nettoie les données de test"""
    try:
        admin_client = get_supabase_admin_client()
        admin_client.auth.admin.delete_user(test_user['id'])
        logger.info("✅ Nettoyage des données de test réussi")
    except Exception as e:
        logger.error(f"⚠️ Erreur lors du nettoyage: {str(e)}")

def run_all_tests():
    """Exécute tous les tests"""
    logger.info("🚀 Démarrage des tests...")
    
    # 1. Tests d'authentification
    access_token, test_user = test_auth()
    if not access_token:
        logger.error("❌ Tests d'authentification échoués")
        return False
        
    # 2. Tests des opérations sur les produits
    if not test_product_operations(access_token):
        logger.error("❌ Tests des opérations sur les produits échoués")
        return False
        
    # 3. Nettoyage
    cleanup_test_user(test_user)
    
    logger.info("✅ Tous les tests ont réussi!")
    return True

if __name__ == "__main__":
    run_all_tests()
