from django.core.management.base import BaseCommand
from django.conf import settings
from main.supabase_adapter import SupabaseAdapter
import logging

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Charge les données de test dans la base de données'

    def handle(self, *args, **kwargs):
        db = SupabaseAdapter()
        self.stdout.write('Chargement des données de test...')
        
        try:
            # Ajout des catégories
            self.stdout.write('\nAjout des catégories...')
            categories = [
                {"name": "Outillage à main", "slug": "outillage-main", "description": "Outils manuels pour tous vos travaux"},
                {"name": "Électroportatif", "slug": "electroportatif", "description": "Outils électriques professionnels"},
                {"name": "Quincaillerie", "slug": "quincaillerie", "description": "Visserie et accessoires"},
                {"name": "Peinture", "slug": "peinture", "description": "Peintures et accessoires"},
                {"name": "Jardinage", "slug": "jardinage", "description": "Outils de jardinage"}
            ]
            
            for category in categories:
                try:
                    result = db.supabase.table('categories').insert(category).execute()
                    self.stdout.write(self.style.SUCCESS(f"✓ Catégorie ajoutée : {category['name']}"))
                except Exception as e:
                    if "duplicate key" in str(e):
                        self.stdout.write(self.style.WARNING(f"! Catégorie déjà existante : {category['name']}"))
                    else:
                        self.stdout.write(self.style.ERROR(f"✗ Erreur lors de l'ajout de {category['name']}: {str(e)}"))
            
            # Ajout des marques
            self.stdout.write('\nAjout des marques...')
            brands = [
                {"name": "Stanley", "slug": "stanley", "description": "Outillage professionnel"},
                {"name": "Bosch", "slug": "bosch", "description": "Leader de l'électroportatif"},
                {"name": "Facom", "slug": "facom", "description": "Outillage de qualité"},
                {"name": "Makita", "slug": "makita", "description": "Outils électroportatifs professionnels"},
                {"name": "DeWalt", "slug": "dewalt", "description": "Outillage électroportatif professionnel"}
            ]
            
            for brand in brands:
                try:
                    result = db.supabase.table('brands').insert(brand).execute()
                    self.stdout.write(self.style.SUCCESS(f"✓ Marque ajoutée : {brand['name']}"))
                except Exception as e:
                    if "duplicate key" in str(e):
                        self.stdout.write(self.style.WARNING(f"! Marque déjà existante : {brand['name']}"))
                    else:
                        self.stdout.write(self.style.ERROR(f"✗ Erreur lors de l'ajout de {brand['name']}: {str(e)}"))
            
            # Récupérer les IDs des catégories et marques
            db_categories = db.get_categories()
            db_brands = db.get_brands()
            
            # Créer un mapping pour faciliter l'accès aux IDs
            category_map = {cat['slug']: cat['id'] for cat in db_categories}
            brand_map = {brand['slug']: brand['id'] for brand in db_brands}
            
            # Ajout des produits
            self.stdout.write('\nAjout des produits...')
            products = [
                {
                    "name": "Marteau de charpentier Stanley",
                    "slug": "marteau-stanley",
                    "description": "Marteau robuste avec manche en bois",
                    "price": 29.99,
                    "category_id": category_map['outillage-main'],
                    "brand_id": brand_map['stanley'],
                    "image_url": "https://example.com/images/marteau-stanley.jpg",
                    "is_active": True
                },
                {
                    "name": "Perceuse-visseuse Bosch GSR 18V",
                    "slug": "perceuse-bosch-gsr18v",
                    "description": "Perceuse sans fil 18V avec 2 batteries",
                    "price": 199.99,
                    "category_id": category_map['electroportatif'],
                    "brand_id": brand_map['bosch'],
                    "image_url": "https://example.com/images/perceuse-bosch.jpg",
                    "is_active": True
                },
                {
                    "name": "Clé à molette Facom",
                    "slug": "cle-molette-facom",
                    "description": "Clé à molette professionnelle",
                    "price": 39.99,
                    "category_id": category_map['outillage-main'],
                    "brand_id": brand_map['facom'],
                    "image_url": "https://example.com/images/cle-facom.jpg",
                    "is_active": True
                }
            ]
            
            for product in products:
                try:
                    # Ajouter le produit
                    result = db.supabase.table('products').insert(product).execute()
                    product_id = result.data[0]['id']
                    
                    # Ajouter l'inventaire initial
                    inventory = {
                        "product_id": product_id,
                        "quantity": 50,
                        "min_quantity": 10
                    }
                    db.supabase.table('inventory').insert(inventory).execute()
                    
                    self.stdout.write(self.style.SUCCESS(f"✓ Produit ajouté : {product['name']}"))
                except Exception as e:
                    if "duplicate key" in str(e):
                        self.stdout.write(self.style.WARNING(f"! Produit déjà existant : {product['name']}"))
                    else:
                        self.stdout.write(self.style.ERROR(f"✗ Erreur lors de l'ajout de {product['name']}: {str(e)}"))
            
            self.stdout.write(self.style.SUCCESS('\nChargement des données de test terminé avec succès!'))
