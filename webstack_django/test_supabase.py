from main.supabase_config import test_supabase_connection, get_supabase_client
import logging

# Configuration du logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_all():
    """Teste toutes les fonctionnalités Supabase"""
    try:
        # 1. Test de la connexion
        logger.info("Test de la connexion à Supabase...")
        if not test_supabase_connection():
            logger.error("❌ Échec de la connexion à Supabase")
            return False
        logger.info("✅ Connexion à Supabase réussie")
        
        # 2. Test des tables
        client = get_supabase_client()
        
        # Test des catégories
        logger.info("Test de la table categories...")
        categories = client.table('categories').select('*').execute()
        logger.info(f"✅ {len(categories.data)} catégories trouvées")
        
        # Test des marques
        logger.info("Test de la table brands...")
        brands = client.table('brands').select('*').execute()
        logger.info(f"✅ {len(brands.data)} marques trouvées")
        
        # Test des produits
        logger.info("Test de la table products...")
        products = client.table('products').select('*').execute()
        logger.info(f"✅ {len(products.data)} produits trouvés")
        
        logger.info("✅ Tous les tests ont réussi!")
        return True
        
    except Exception as e:
        logger.error(f"❌ Erreur lors des tests: {str(e)}")
        return False

if __name__ == "__main__":
    test_all()
