import os
import json
import requests
from django.core.management.base import BaseCommand
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile
from main.models import Category, Product
from django.conf import settings

class Command(BaseCommand):
    help = 'Import sample data and download images'

    def handle(self, *args, **options):
        # Créer les dossiers médias
        os.makedirs(os.path.join(settings.MEDIA_ROOT, 'products'), exist_ok=True)
        os.makedirs(os.path.join(settings.MEDIA_ROOT, 'categories'), exist_ok=True)

        # Charger les données
        fixture_path = os.path.join(settings.BASE_DIR, 'main', 'fixtures', 'sample_data.json')
        with open(fixture_path, 'r', encoding='utf-8') as file:
            data = json.load(file)

        # Traiter les données
        for item in data:
            if item['model'] == 'main.category':
                self._process_category(item)
            elif item['model'] == 'main.product':
                self._process_product(item)

        self.stdout.write(self.style.SUCCESS('Successfully imported sample data'))

    def _process_category(self, item):
        fields = item['fields']
        category, created = Category.objects.update_or_create(
            id=item['pk'],
            defaults={
                'name': fields['name'],
                'slug': fields['slug'],
                'description': fields['description'],
                'featured_brands': fields.get('featured_brands', []),
                'tips': fields.get('tips', [])
            }
        )
        
        if 'image_url' in fields:
            self._download_image(fields['image_url'], category, 'image')

    def _process_product(self, item):
        fields = item['fields']
        product, created = Product.objects.update_or_create(
            id=item['pk'],
            defaults={
                'category_id': fields['category'],
                'name': fields['name'],
                'slug': fields['slug'],
                'description': fields['description'],
                'specifications': fields.get('specifications', []),
                'price': fields['price'],
                'stock': fields['stock'],
                'is_new': fields.get('is_new', False),
                'rating': fields.get('rating', '0.00')
            }
        )
        
        if 'image_url' in fields:
            self._download_image(fields['image_url'], product, 'image')

    def _download_image(self, url, instance, field_name):
        try:
            # Ajouter les paramètres pour Unsplash
            url = f"{url}?auto=format&fit=crop&w=800&q=80"
            
            response = requests.get(url)
            if response.status_code == 200:
                img_temp = NamedTemporaryFile(delete=True)
                img_temp.write(response.content)
                img_temp.flush()
                
                # Générer un nom de fichier unique
                file_name = f"{instance.__class__.__name__.lower()}_{instance.id}.jpg"
                
                # Sauvegarder l'image
                getattr(instance, field_name).save(file_name, File(img_temp), save=True)
                
                self.stdout.write(
                    self.style.SUCCESS(f'Successfully downloaded image for {instance}')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'Failed to download image for {instance}')
                )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error downloading image: {str(e)}')
            )
