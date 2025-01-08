import os
import django
from decimal import Decimal

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'webstack_django.settings')
django.setup()

from django.contrib.auth.models import User
from main.models import Category, Brand, Product

def create_superuser():
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
        print("Superutilisateur créé avec succès!")

def create_sample_data():
    # Création des catégories
    categories_data = [
        {
            'name': 'Nettoyants',
            'description': 'Produits de nettoyage pour toutes les surfaces'
        },
        {
            'name': 'Lessives',
            'description': 'Produits pour le linge et la lessive'
        },
        {
            'name': 'Entretien',
            'description': 'Produits d\'entretien spécialisés'
        }
    ]
    
    categories = {}
    for cat_data in categories_data:
        cat, created = Category.objects.get_or_create(
            name=cat_data['name'],
            defaults={'description': cat_data['description']}
        )
        categories[cat_data['name']] = cat
        print(f"Catégorie {'créée' if created else 'existante'}: {cat.name}")

    # Création des marques
    brands_data = [
        {
            'name': 'Clean & Fresh',
            'description': 'Produits écologiques de haute qualité'
        },
        {
            'name': 'BrightHome',
            'description': 'Solutions de nettoyage professionnelles'
        },
        {
            'name': 'EcoWash',
            'description': 'Produits respectueux de l\'environnement'
        }
    ]
    
    brands = {}
    for brand_data in brands_data:
        brand, created = Brand.objects.get_or_create(
            name=brand_data['name'],
            defaults={'description': brand_data['description']}
        )
        brands[brand_data['name']] = brand
        print(f"Marque {'créée' if created else 'existante'}: {brand.name}")

    # Création des produits
    products_data = [
        {
            'name': 'Nettoyant Multi-surfaces',
            'description': 'Nettoie et désinfecte toutes les surfaces',
            'price': '4.99',
            'stock': 100,
            'category': 'Nettoyants',
            'brand': 'Clean & Fresh'
        },
        {
            'name': 'Lessive Écologique',
            'description': 'Lessive concentrée pour tous types de textiles',
            'price': '12.99',
            'stock': 50,
            'category': 'Lessives',
            'brand': 'EcoWash'
        },
        {
            'name': 'Détartrant WC',
            'description': 'Élimine efficacement le calcaire',
            'price': '3.99',
            'stock': 75,
            'category': 'Entretien',
            'brand': 'BrightHome'
        },
        {
            'name': 'Spray Désinfectant',
            'description': 'Désinfecte et élimine 99.9% des bactéries',
            'price': '5.99',
            'stock': 60,
            'category': 'Nettoyants',
            'brand': 'Clean & Fresh'
        },
        {
            'name': 'Assouplissant Natural',
            'description': 'Parfum naturel de lavande',
            'price': '8.99',
            'stock': 40,
            'category': 'Lessives',
            'brand': 'EcoWash'
        }
    ]

    for prod_data in products_data:
        product, created = Product.objects.get_or_create(
            name=prod_data['name'],
            defaults={
                'description': prod_data['description'],
                'price': Decimal(prod_data['price']),
                'stock': prod_data['stock'],
                'category': categories[prod_data['category']],
                'brand': brands[prod_data['brand']]
            }
        )
        print(f"Produit {'créé' if created else 'existant'}: {product.name}")

if __name__ == '__main__':
    print("Création du superutilisateur...")
    create_superuser()
    print("\nCréation des données d'exemple...")
    create_sample_data()
    print("\nConfiguration terminée!")
