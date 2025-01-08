import os
import requests
from django.core.management.base import BaseCommand
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile
from main.models import Product, Category
from django.conf import settings

class Command(BaseCommand):
    help = 'Fetch product images from Unsplash API'

    def add_arguments(self, parser):
        parser.add_argument('--access-key', type=str, help='Unsplash API access key')

    def handle(self, *args, **options):
        access_key = options.get('access_key') or os.getenv('UNSPLASH_ACCESS_KEY')
        
        if not access_key:
            self.stdout.write(self.style.ERROR('No Unsplash access key provided'))
            return

        # Créer les dossiers médias s'ils n'existent pas
        os.makedirs(os.path.join(settings.MEDIA_ROOT, 'products'), exist_ok=True)
        os.makedirs(os.path.join(settings.MEDIA_ROOT, 'categories'), exist_ok=True)

        # Mettre à jour les images des produits
        for product in Product.objects.filter(image=''):
            self._fetch_product_image(product, access_key)

        # Mettre à jour les images des catégories
        for category in Category.objects.filter(image=''):
            self._fetch_category_image(category, access_key)

    def _fetch_product_image(self, product, access_key):
        search_term = f"{product.name} product"
        self._fetch_and_save_image(product, search_term, access_key, 'image')

    def _fetch_category_image(self, category, access_key):
        search_term = f"{category.name} category"
        self._fetch_and_save_image(category, search_term, access_key, 'image')

    def _fetch_and_save_image(self, instance, search_term, access_key, field_name):
        try:
            # Appeler l'API Unsplash
            url = f"https://api.unsplash.com/search/photos"
            headers = {"Authorization": f"Client-ID {access_key}"}
            params = {
                "query": search_term,
                "per_page": 1,
                "orientation": "landscape"
            }
            
            response = requests.get(url, headers=headers, params=params)
            
            if response.status_code == 200:
                data = response.json()
                if data['results']:
                    image_url = data['results'][0]['urls']['regular']
                    
                    # Télécharger l'image
                    img_response = requests.get(image_url)
                    if img_response.status_code == 200:
                        img_temp = NamedTemporaryFile(delete=True)
                        img_temp.write(img_response.content)
                        img_temp.flush()
                        
                        # Générer un nom de fichier unique
                        file_name = f"{instance.__class__.__name__.lower()}_{instance.id}.jpg"
                        
                        # Sauvegarder l'image
                        getattr(instance, field_name).save(file_name, File(img_temp), save=True)
                        
                        self.stdout.write(self.style.SUCCESS(
                            f'Successfully downloaded image for {instance}'
                        ))
                    else:
                        self.stdout.write(self.style.WARNING(
                            f'Failed to download image for {instance}'
                        ))
                else:
                    self.stdout.write(self.style.WARNING(
                        f'No images found for {instance}'
                    ))
            else:
                self.stdout.write(self.style.ERROR(
                    f'API request failed for {instance}'
                ))
        except Exception as e:
            self.stdout.write(self.style.ERROR(
                f'Error processing {instance}: {str(e)}'
            ))
