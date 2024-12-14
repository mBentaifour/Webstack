from django.db import models
from django.core.validators import MinValueValidator
from .utils import resize_image, create_thumbnail

# Create your models here.

class Product(models.Model):
    CATEGORY_CHOICES = [
        ('nettoyage', 'Nettoyage'),
        ('bricolage', 'Bricolage'),
        ('jardinage', 'Jardinage'),
    ]

    name = models.CharField(max_length=100, verbose_name="Nom")
    description = models.TextField(verbose_name="Description")
    price = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        validators=[MinValueValidator(0)],
        verbose_name="Prix"
    )
    stock = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0)],
        verbose_name="Stock"
    )
    category = models.CharField(
        max_length=50,
        choices=CATEGORY_CHOICES,
        verbose_name="Catégorie"
    )
    image = models.ImageField(
        upload_to='products/',
        null=True,
        blank=True,
        verbose_name="Image"
    )
    thumbnail = models.ImageField(
        upload_to='products/thumbnails/',
        null=True,
        blank=True,
        verbose_name="Miniature"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Produit"
        verbose_name_plural = "Produits"
        ordering = ['-created_at']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.image:
            # Redimensionner l'image principale
            self.image = resize_image(self.image)
            
            # Créer une miniature si elle n'existe pas
            if not self.thumbnail:
                self.thumbnail = create_thumbnail(self.image)
        
        super().save(*args, **kwargs)

    @property
    def image_url(self):
        if self.image:
            return self.image.url
        return None

    @property
    def thumbnail_url(self):
        if self.thumbnail:
            return self.thumbnail.url
        return self.image_url if self.image else None
