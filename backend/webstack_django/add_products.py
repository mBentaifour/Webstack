import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'webstack_django.settings')
django.setup()

from main.models import Product
from decimal import Decimal

# Création des produits
products = [
    {
        'name': 'MIAFOUR - Décapant des Fours et Grils',
        'description': 'Décapant professionnel pour le nettoyage des fours et grils. Contient de l\'hydroxyde de sodium. Biodégradabilité supérieur à 90%.',
        'price': Decimal('24.99'),
        'stock': 50,
        'category': 'Nettoyage',
    },
    {
        'name': 'NOBLA - Liquide Vaisselle Citron',
        'description': 'Liquide vaisselle parfumé au citron. Efficace contre la graisse. Format économique de 5L.',
        'price': Decimal('19.99'),
        'stock': 100,
        'category': 'Nettoyage',
    },
    {
        'name': 'Balai Serpillère Premium',
        'description': 'Balai serpillère avec manche télescopique et tête microfibre. Idéal pour tous types de sols.',
        'price': Decimal('15.99'),
        'stock': 75,
        'category': 'Nettoyage',
    },
    {
        'name': 'Évier Inox avec Égouttoir',
        'description': 'Évier en acier inoxydable avec égouttoir intégré. Installation facile, finition brossée.',
        'price': Decimal('89.99'),
        'stock': 25,
        'category': 'Bricolage',
    },
    {
        'name': 'Évier Simple Bac Inox',
        'description': 'Évier simple bac en acier inoxydable. Design moderne et élégant, installation encastrée.',
        'price': Decimal('79.99'),
        'stock': 30,
        'category': 'Bricolage',
    }
]

# Ajout des produits à la base de données
for product_data in products:
    product = Product(**product_data)
    product.save()
    print(f"Produit créé : {product.name}")
