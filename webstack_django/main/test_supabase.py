from supabase_adapter import SupabaseAdapter
from supabase_config import get_supabase_client
import os
import logging
import uuid
from pathlib import Path

# Configuration du logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Chemin absolu vers le fichier .env
ENV_PATH = Path(__file__).parent.parent / '.env'
logger.info(f"Chemin du fichier .env: {ENV_PATH}")

def authenticate_admin():
    """Authentifie l'administrateur"""
    try:
        # Credentials en dur pour le test
        admin_email = "bentaifourmoh@gmail.com"
        admin_password = "AdminDroguerie2024!"
        
        logger.info(f"Tentative d'authentification avec l'email: {admin_email}")
        
        supabase = get_supabase_client()
        auth_response = supabase.auth.sign_in_with_password({
            "email": admin_email,
            "password": admin_password
        })
        
        if auth_response.user:
            logger.info("✅ Authentification admin réussie!")
            return True
        else:
            logger.error("❌ Échec de l'authentification admin")
            return False
            
    except Exception as e:
        logger.error(f"❌ Erreur lors de l'authentification: {str(e)}")
        return False

def test_supabase_connection():
    """Test de la connexion à Supabase"""
    try:
        db = SupabaseAdapter()
        response = db.get_products(limit=1)
        
        if response.get("success"):
            logger.info("✅ Connexion à Supabase réussie!")
            return True
        else:
            logger.error("❌ Échec de la connexion à Supabase")
            return False
            
    except Exception as e:
        logger.error(f"❌ Erreur de connexion à Supabase: {str(e)}")
        return False

def test_crud_operations():
    """Test des opérations CRUD sur les produits"""
    db = SupabaseAdapter()
    test_results = []

    # 1. Test création d'une catégorie
    category_data = {
        "name": "Test Category",
        "description": "Category for testing"
    }
    category_result = db.create_category(category_data)
    test_results.append(("Création catégorie", category_result.get("success", False)))
    
    if not category_result.get("success"):
        logger.error("❌ Échec de la création de la catégorie, arrêt des tests")
        return test_results

    category_id = category_result["data"]["id"]

    # 2. Test création d'une marque
    brand_data = {
        "name": "Test Brand",
        "description": "Brand for testing"
    }
    brand_result = db.create_brand(brand_data)
    test_results.append(("Création marque", brand_result.get("success", False)))
    
    if not brand_result.get("success"):
        logger.error("❌ Échec de la création de la marque, arrêt des tests")
        return test_results

    brand_id = brand_result["data"]["id"]

    # 3. Test création d'un produit
    product_data = {
        "name": "Test Product",
        "description": "Product for testing",
        "price": 99.99,
        "stock": 10,
        "category_id": category_id,
        "brand_id": brand_id,
        "is_active": True
    }
    
    create_result = db.create_product(product_data)
    test_results.append(("Création produit", create_result.get("success", False)))
    
    if not create_result.get("success"):
        logger.error("❌ Échec de la création du produit, arrêt des tests")
        return test_results

    product_id = create_result["data"]["id"]

    # 4. Test lecture du produit
    read_result = db.get_product_by_id(product_id)
    test_results.append(("Lecture produit", read_result.get("success", False)))

    # 5. Test mise à jour du produit
    update_data = {
        "price": 89.99,
        "description": "Updated test product"
    }
    update_result = db.update_product(product_id, update_data)
    test_results.append(("Mise à jour produit", update_result.get("success", False)))

    # 6. Test filtrage des produits
    filter_result = db.get_products(
        limit=10,
        category_id=category_id,
        min_price=80,
        max_price=100,
        sort_by="price_asc"
    )
    test_results.append(("Filtrage produits", filter_result.get("success", False)))

    # 7. Test soft delete du produit
    delete_result = db.delete_product(product_id)
    test_results.append(("Suppression produit", delete_result.get("success", False)))

    return test_results

def run_all_tests():
    """Exécute tous les tests"""
    logger.info("🚀 Démarrage des tests...")
    
    # Authentification admin
    if not authenticate_admin():
        logger.error("❌ Tests arrêtés en raison de l'échec de l'authentification")
        return
    
    # Test de connexion
    if not test_supabase_connection():
        logger.error("❌ Tests arrêtés en raison de l'échec de la connexion")
        return
    
    # Test des opérations CRUD
    results = test_crud_operations()
    
    # Affichage des résultats
    logger.info("\n=== Résultats des tests ===")
    for test_name, success in results:
        status = "✅" if success else "❌"
        logger.info(f"{status} {test_name}")
    
    # Calcul du taux de réussite
    if results:
        success_rate = (len([r for _, r in results if r]) / len(results)) * 100
        logger.info(f"\nTaux de réussite: {success_rate:.1f}%")

if __name__ == "__main__":
    run_all_tests()
