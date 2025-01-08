import os
import requests
from django.core.management.base import BaseCommand
from django.core.files import File
from django.conf import settings
from main.models import Category, Product
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Download sample images for products and categories with improved error handling'

    def add_arguments(self, parser):
        parser.add_argument(
            '--force',
            action='store_true',
            help='Force download even if images already exist',
        )

    def handle(self, *args, **options):
        force = options.get('force', False)
        
        # Ensure media directories exist
        self._create_media_directories()

        # Configuration des images
        images_config = {
            'categories': {
                'Peinture et Décoration': 'https://images.unsplash.com/photo-1589939705384-5185137a7f0f',
                'Électricité': 'https://images.unsplash.com/photo-1555664424-778a1e5e1b48',
                'Quincaillerie': 'https://images.unsplash.com/photo-1621905252507-b35492cc74b4'
            },
            'products': {
                'Peinture Mate Blanche 10L': 'https://images.unsplash.com/photo-1562259949-e8e7689d7828',
                'Kit Rouleaux et Pinceaux': 'https://images.unsplash.com/photo-1597484661643-2f5fef640dd1',
                'Dévisseuse Bosch': 'https://images.unsplash.com/photo-1504148455328-c376907d081c'
            }
        }

        # Téléchargement des images pour les catégories
        self._process_categories(images_config['categories'], force)
        
        # Téléchargement des images pour les produits
        self._process_products(images_config['products'], force)

    def _create_media_directories(self):
        """Crée les répertoires nécessaires pour les médias"""
        directories = [
            os.path.join(settings.MEDIA_ROOT),
            os.path.join(settings.MEDIA_ROOT, 'products'),
            os.path.join(settings.MEDIA_ROOT, 'categories')
        ]
        for directory in directories:
            if not os.path.exists(directory):
                os.makedirs(directory)
                logger.info(f"Créé le répertoire: {directory}")

    def _download_image(self, url, filename):
        """Télécharge une image depuis une URL"""
        try:
            # Ajouter les paramètres pour Unsplash
            url = f"{url}?auto=format&fit=crop&w=800&q=80"
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            
            # Sauvegarder l'image
            with open(filename, 'wb') as f:
                f.write(response.content)
            return True
        except requests.exceptions.RequestException as e:
            logger.error(f"Erreur lors du téléchargement de {url}: {str(e)}")
            return False

    def _process_categories(self, category_images, force):
        """Traite les images des catégories"""
        for category in Category.objects.all():
            if str(category.name) in category_images:
                image_url = category_images[str(category.name)]
                image_path = os.path.join(settings.MEDIA_ROOT, 'categories', f"{category.slug}.jpg")
                
                if not os.path.exists(image_path) or force:
                    logger.info(f"Téléchargement de l'image pour la catégorie: {category.name}")
                    if self._download_image(image_url, image_path):
                        category.image = f"categories/{category.slug}.jpg"
                        category.save()
                        logger.info(f"Image téléchargée avec succès pour {category.name}")
                else:
                    logger.info(f"L'image existe déjà pour {category.name}")

    def _process_products(self, product_images, force):
        """Traite les images des produits"""
        for product in Product.objects.all():
            if str(product.name) in product_images:
                image_url = product_images[str(product.name)]
                image_path = os.path.join(settings.MEDIA_ROOT, 'products', f"{product.slug}.jpg")
                
                if not os.path.exists(image_path) or force:
                    logger.info(f"Téléchargement de l'image pour le produit: {product.name}")
                    if self._download_image(image_url, image_path):
                        product.image = f"products/{product.slug}.jpg"
                        product.save()
                        logger.info(f"Image téléchargée avec succès pour {product.name}")
                else:
                    logger.info(f"L'image existe déjà pour {product.name}")
