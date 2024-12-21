import os
import requests
from django.core.management.base import BaseCommand
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile
from main.models import Category, Product
from django.conf import settings
import urllib.request
import tempfile

class Command(BaseCommand):
    help = 'Download sample images for products and categories'

    def handle(self, *args, **options):
        # Images pour les catégories
        category_images = {
            'Peinture et Décoration': 'https://images.unsplash.com/photo-1589939705384-5185137a7f0f',
            'Électricité': 'https://images.unsplash.com/photo-1555664424-778a1e5e1b48',
            'Quincaillerie': 'https://images.unsplash.com/photo-1621905252507-b35492cc74b4'
        }

        # Images pour les produits
        product_images = {
            'Peinture Mate Blanche 10L': 'https://images.unsplash.com/photo-1562259949-e8e7689d7828',
            'Kit Rouleaux et Pinceaux': 'https://images.unsplash.com/photo-1597484661643-2f5fef640dd1'
        }

        # URL de l'image pour la dévisseuse Bosch (une image générique d'une perceuse)
        bosch_drill_url = "https://images.unsplash.com/photo-1504148455328-c376907d081c"

        # Créer les dossiers médias
        os.makedirs(os.path.join(settings.MEDIA_ROOT, 'products'), exist_ok=True)
        os.makedirs(os.path.join(settings.MEDIA_ROOT, 'categories'), exist_ok=True)

        # Télécharger les images des catégories
        for category in Category.objects.all():
            try:
                if not isinstance(category, Category) or not hasattr(category, 'name'):
                    self.stdout.write(
                        self.style.WARNING(f'Invalid category object: {category}')
                    )
                    continue
                
                if str(category.name) in category_images:
                    self._download_image(
                        category_images[str(category.name)],
                        category,
                        'image',
                        'categories'
                    )
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f'Error processing category: {str(e)}')
                )

        # Télécharger les images des produits
        for product in Product.objects.all():
            try:
                if not isinstance(product, Product) or not hasattr(product, 'name'):
                    self.stdout.write(
                        self.style.WARNING(f'Invalid product object: {product}')
                    )
                    continue
                
                if str(product.name) in product_images:
                    self._download_image(
                        product_images[str(product.name)],
                        product,
                        'image',
                        'products'
                    )
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f'Error processing product: {str(e)}')
                )

        # Télécharger l'image pour la dévisseuse Bosch
        try:
            # Récupérer le produit
            product = Product.objects.get(slug='devisseuse-bosch')
            
            # Télécharger et sauvegarder l'image
            img_temp = NamedTemporaryFile(delete=True)
            img_temp.write(urllib.request.urlopen(bosch_drill_url).read())
            img_temp.flush()
            
            # Sauvegarder l'image dans le champ image du produit
            product.image.save(f"bosch_drill.jpg", File(img_temp), save=True)
            
            self.stdout.write(self.style.SUCCESS(f'Image téléchargée avec succès pour {product.name}'))
            
        except Product.DoesNotExist:
            self.stdout.write(self.style.ERROR('Produit non trouvé'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Erreur lors du téléchargement de l\'image: {str(e)}'))

    def _download_image(self, url, instance, field_name, folder):
        try:
            # Ajouter les paramètres pour Unsplash
            url = f"{url}?auto=format&fit=crop&w=800&q=80"
            
            response = requests.get(url)
            if response.status_code == 200:
                # Utiliser NamedTemporaryFile de Python standard
                with tempfile.NamedTemporaryFile() as img_temp:
                    img_temp.write(response.content)
                    img_temp.flush()
                    
                    # Générer un nom de fichier unique
                    file_name = f"{folder}/{instance.__class__.__name__.lower()}_{instance.id}.jpg"
                    
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
