import os
import json
import requests
from django.core.management.base import BaseCommand
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile
from main.models import Category, Product
from django.conf import settings

class Command(BaseCommand):
    help = 'Import products from JSON file and download images'

    def add_arguments(self, parser):
        parser.add_argument('json_file', type=str, help='Path to JSON file containing product data')

    def handle(self, *args, **options):
        json_file_path = options['json_file']
        
        # Vérifier si le fichier existe
        if not os.path.exists(json_file_path):
            self.stdout.write(self.style.ERROR(f'File {json_file_path} does not exist'))
            return

        # Lire le fichier JSON
        with open(json_file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)

        # Créer les dossiers médias s'ils n'existent pas
        os.makedirs(os.path.join(settings.MEDIA_ROOT, 'products'), exist_ok=True)
        os.makedirs(os.path.join(settings.MEDIA_ROOT, 'categories'), exist_ok=True)

        # Traiter les données
        for item in data:
            if item['model'] == 'main.category':
                self._process_category(item)
            elif item['model'] == 'main.product':
                self._process_product(item)

        self.stdout.write(self.style.SUCCESS('Successfully imported data'))

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
        
        # Si une URL d'image est fournie, la télécharger
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
        
        # Si une URL d'image est fournie, la télécharger
        if 'image_url' in fields:
            self._download_image(fields['image_url'], product, 'image')

    def _download_image(self, url, instance, field_name):
        try:
            response = requests.get(url)
            if response.status_code == 200:
                img_temp = NamedTemporaryFile(delete=True)
                img_temp.write(response.content)
                img_temp.flush()
                
                # Obtenir le nom du fichier depuis l'URL
                file_name = os.path.basename(url)
                
                # Sauvegarder l'image
                getattr(instance, field_name).save(file_name, File(img_temp), save=True)
                
                self.stdout.write(self.style.SUCCESS(f'Successfully downloaded image for {instance}'))
            else:
                self.stdout.write(self.style.WARNING(f'Failed to download image from {url}'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error downloading image: {str(e)}'))
