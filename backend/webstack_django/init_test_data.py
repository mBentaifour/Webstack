import os
import django
from django.core.files import File
from django.contrib.auth.models import User
from pathlib import Path

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'webstack_django.settings')
django.setup()

from main.models import Category, Product, Brand

def create_superuser():
    try:
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('admin', 'admin@example.com', 'Admin@123')
            print("Superuser créé avec succès!")
    except Exception as e:
        print(f"Erreur lors de la création du superuser: {e}")

def create_test_data():
    # Création des catégories
    categories_data = [
        {
            'name': 'Ordinateurs Portables',
            'description': 'Ordinateurs portables pour tous les besoins'
        },
        {
            'name': 'Smartphones',
            'description': 'Téléphones intelligents de dernière génération'
        },
        {
            'name': 'Accessoires',
            'description': 'Accessoires pour vos appareils électroniques'
        }
    ]

    categories = []
    for cat_data in categories_data:
        category, created = Category.objects.get_or_create(
            name=cat_data['name'],
            defaults={
                'description': cat_data['description'],
                'slug': django.utils.text.slugify(cat_data['name'])
            }
        )
        categories.append(category)
        print(f"Catégorie {'créée' if created else 'existante'}: {category.name}")

    # Création des produits
    products_data = [
        {
            'name': 'MacBook Pro 16"',
            'description': 'Portable puissant avec écran Retina',
            'price': 2499.99,
            'stock': 10,
            'category': categories[0],
            'is_new': True,
            'is_sale': False
        },
        {
            'name': 'iPhone 15 Pro',
            'description': 'Dernier iPhone avec appareil photo professionnel',
            'price': 1299.99,
            'stock': 15,
            'category': categories[1],
            'is_new': True,
            'is_sale': False
        },
        {
            'name': 'Samsung Galaxy S23',
            'description': 'Smartphone Android haut de gamme',
            'price': 999.99,
            'stock': 8,
            'category': categories[1],
            'is_new': False,
            'is_sale': True
        },
        {
            'name': 'AirPods Pro',
            'description': 'Écouteurs sans fil avec réduction de bruit',
            'price': 249.99,
            'stock': 20,
            'category': categories[2],
            'is_new': False,
            'is_sale': True
        }
    ]

    for prod_data in products_data:
        product, created = Product.objects.get_or_create(
            name=prod_data['name'],
            defaults={
                'description': prod_data['description'],
                'price': prod_data['price'],
                'stock': prod_data['stock'],
                'category': prod_data['category'],
                'is_new': prod_data.get('is_new', False),
                'is_sale': prod_data.get('is_sale', False),
                'slug': django.utils.text.slugify(prod_data['name'])
            }
        )
        print(f"Produit {'créé' if created else 'existant'}: {product.name}")

if __name__ == '__main__':
    print("Création du superuser...")
    create_superuser()
    print("\nCréation des données de test...")
    create_test_data()
    print("\nConfiguration terminée!")
