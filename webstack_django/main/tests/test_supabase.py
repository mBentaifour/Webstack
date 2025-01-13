import logging
from pathlib import Path
from ..supabase_adapter import SupabaseAdapter

# Configuration du logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Chemin absolu vers le fichier .env
ENV_PATH = Path(__file__).parent.parent.parent / '.env'
logger.info(f"Chemin du fichier .env: {ENV_PATH}")

def test_connection():
    """Test de la connexion à Supabase"""
    try:
        db = SupabaseAdapter()
        categories = db.get_categories()
        
        if categories is not None:
            logger.info("✅ Connexion à Supabase réussie!")
            logger.info(f"Nombre de catégories trouvées: {len(categories)}")
            return True
        else:
            logger.error("❌ Échec de la connexion à Supabase")
            return False
            
    except Exception as e:
        logger.error(f"❌ Erreur lors de la connexion: {str(e)}")
        return False

def test_crud_operations():
    """Test des opérations CRUD"""
    try:
        db = SupabaseAdapter()
        
        # Test de récupération des catégories
        categories = db.get_categories()
        logger.info(f"✅ {len(categories)} catégories trouvées")
        
        # Test de récupération des marques
        brands = db.get_brands()
        logger.info(f"✅ {len(brands)} marques trouvées")
        
        # Test de récupération des produits
        products = db.get_products()
        logger.info(f"✅ {len(products)} produits trouvés")
        
        if products:
            # Test de récupération d'un produit spécifique
            product = db.get_product_by_id(products[0]['id'])
            logger.info(f"✅ Produit trouvé: {product['name'] if product else 'Non trouvé'}")
            
            # Test de récupération de l'inventaire
            inventory = db.get_inventory(products[0]['id'])
            logger.info(f"✅ Inventaire trouvé: {inventory['quantity'] if inventory else 'Non trouvé'}")
        
        return True
            
    except Exception as e:
        logger.error(f"❌ Erreur lors des tests CRUD: {str(e)}")
        return False

def run_all_tests():
    """Exécute tous les tests"""
    tests = [
        ("Test de connexion", test_connection),
        ("Test des opérations CRUD", test_crud_operations),
    ]
    
    success = True
    for test_name, test_func in tests:
        logger.info(f"\nExécution du test: {test_name}")
        if not test_func():
            success = False
            logger.error(f"❌ {test_name} a échoué")
        else:
            logger.info(f"✅ {test_name} réussi")
    
    return success

if __name__ == "__main__":
    run_all_tests()
