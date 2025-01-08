import requests
import json
import time

BASE_URL = "http://localhost:8000/api"

def test_get_all_products():
    print("\n1. Test: Récupération de tous les produits")
    response = requests.get(f"{BASE_URL}/products/")
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        products = response.json()
        print(f"Nombre de produits: {len(products)}")
        if len(products) > 0:
            print("Premier produit:", json.dumps(products[0], indent=2))
    else:
        print("Erreur:", response.text)
    return response.json() if response.status_code == 200 else None

def test_create_product():
    print("\n2. Test: Création d'un nouveau produit")
    new_product = {
        "name": "Testeur électrique digital",
        "slug": "testeur-electrique-digital",
        "description": "Testeur électrique professionnel avec écran LCD",
        "price": 89.99,
        "stock": 30,
        "category_id": "29bf495e-eb1c-43b1-b753-80a937129628"  # Catégorie "Mesure et traçage"
    }
    
    response = requests.post(f"{BASE_URL}/products/", json=new_product)
    print(f"Status: {response.status_code}")
    if response.status_code in [200, 201]:
        print("Produit créé:", json.dumps(response.json(), indent=2))
        return response.json()
    else:
        print("Erreur:", response.text)
        return None

def test_update_product(product_id):
    print("\n3. Test: Mise à jour d'un produit")
    update_data = {
        "price": 94.99,
        "stock": 25,
        "description": "Testeur électrique professionnel avec écran LCD et fonction auto-range"
    }
    
    response = requests.put(f"{BASE_URL}/products/{product_id}/", json=update_data)
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        print("Produit mis à jour:", json.dumps(response.json(), indent=2))
        return response.json()
    else:
        print("Erreur:", response.text)
        return None

def test_delete_product(product_id):
    print("\n4. Test: Suppression d'un produit")
    response = requests.delete(f"{BASE_URL}/products/{product_id}/")
    print(f"Status: {response.status_code}")
    if response.status_code in [200, 204]:
        print("Produit supprimé avec succès")
        return True
    else:
        print("Erreur:", response.text)
        return False

def verify_deletion(product_id):
    print("\n5. Test: Vérification de la suppression")
    response = requests.get(f"{BASE_URL}/products/{product_id}/")
    if response.status_code == 404:
        print("Confirmation: Le produit n'existe plus")
        return True
    else:
        print("Erreur: Le produit existe encore")
        return False

def test_get_single_product():
    print("\n6. Test: Récupération d'un produit spécifique")
    # Utiliser l'ID du premier produit obtenu précédemment
    response = requests.get(f"{BASE_URL}/products/")
    if response.status_code == 200:
        products = response.json()
        if len(products) > 0:
            product_id = products[0]['id']
            response = requests.get(f"{BASE_URL}/products/{product_id}/")
            print(f"Status: {response.status_code}")
            if response.status_code == 200:
                print("Produit trouvé:", json.dumps(response.json(), indent=2))
            else:
                print("Erreur:", response.text)
    else:
        print("Erreur lors de la récupération des produits")

def test_search_products():
    print("\n7. Test: Recherche de produits")
    search_term = "marteau"
    response = requests.post(
        f"{BASE_URL}/products/search/",
        json={"search": search_term}
    )
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        results = response.json()
        print(f"Résultats pour '{search_term}':", json.dumps(results, indent=2))
    else:
        print("Erreur:", response.text)

if __name__ == "__main__":
    print("=== Test complet des endpoints de l'API produits ===")
    
    # Test GET all
    products = test_get_all_products()
    
    # Test CREATE
    new_product = test_create_product()
    if new_product:
        time.sleep(1)  # Petite pause pour s'assurer que la création est bien terminée
        
        # Test UPDATE
        updated_product = test_update_product(new_product['id'])
        if updated_product:
            time.sleep(1)  # Petite pause pour s'assurer que la mise à jour est bien terminée
            
            # Test DELETE
            if test_delete_product(new_product['id']):
                time.sleep(1)  # Petite pause pour s'assurer que la suppression est bien terminée
                verify_deletion(new_product['id'])
    
    # Test GET single
    test_get_single_product()
    
    # Test SEARCH
    test_search_products()
    
    print("\n=== Tests terminés ===")
