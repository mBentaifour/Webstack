from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.urls import reverse
from django.utils import timezone
from .utils import resize_image, create_thumbnail
import uuid

class Category(models.Model):
    CATEGORY_TYPES = [
        ('hand_tools', 'Outils à main'),
        ('power_tools', 'Outils électriques'),
        ('measuring', 'Mesure et traçage'),
        ('safety', 'Sécurité et protection'),
        ('hardware', 'Quincaillerie'),
        ('garden', 'Jardin'),
        ('workshop', 'Atelier'),
        ('plumbing', 'Plomberie'),
        ('electrical', 'Électricité'),
        ('painting', 'Peinture'),
    ]

    name = models.CharField(max_length=200, verbose_name="Nom")
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    category_type = models.CharField(max_length=50, choices=CATEGORY_TYPES, verbose_name="Type de catégorie")
    description = models.TextField(blank=True, verbose_name="Description")
    image = models.ImageField(upload_to='categories/', blank=True, null=True)
    icon = models.CharField(max_length=50, blank=True, help_text="Classe d'icône (ex: fas fa-wrench)")
    featured_brands = models.JSONField(default=list, blank=True)
    discount_count = models.IntegerField(default=0)
    tips = models.JSONField(default=list, blank=True, help_text="Conseils d'utilisation pour cette catégorie")
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']
        verbose_name = "Catégorie"
        verbose_name_plural = 'Catégories'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('main:category_detail', args=[self.slug])

class Brand(models.Model):
    QUALITY_CHOICES = [
        ('premium', 'Premium'),
        ('professional', 'Professionnel'),
        ('standard', 'Standard'),
    ]

    name = models.CharField(max_length=200, verbose_name="Nom")
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    logo = models.ImageField(upload_to='brands/', blank=True, null=True)
    description = models.TextField(blank=True, verbose_name="Description")
    website = models.URLField(blank=True)
    quality_tier = models.CharField(max_length=20, choices=QUALITY_CHOICES, default='standard')
    country_of_origin = models.CharField(max_length=100, blank=True, verbose_name="Pays d'origine")
    warranty_info = models.TextField(blank=True, verbose_name="Information de garantie")
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name = "Marque"
        verbose_name_plural = "Marques"
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

class Product(models.Model):
    USAGE_TYPE = [
        ('professional', 'Professionnel'),
        ('diy', 'Bricolage'),
        ('industrial', 'Industriel'),
    ]
    
    POWER_SOURCE = [
        ('manual', 'Manuel'),
        ('electric', 'Électrique'),
        ('battery', 'Batterie'),
        ('pneumatic', 'Pneumatique'),
    ]

    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE, verbose_name="Catégorie")
    brand = models.ForeignKey(Brand, related_name='products', on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Marque")
    name = models.CharField(max_length=200, verbose_name="Nom")
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    description = models.TextField(verbose_name="Description")
    usage_type = models.CharField(max_length=20, choices=USAGE_TYPE, default='diy', verbose_name="Type d'utilisation")
    power_source = models.CharField(max_length=20, choices=POWER_SOURCE, default='manual', verbose_name="Source d'énergie")
    specifications = models.JSONField(default=dict, blank=True, help_text="Caractéristiques techniques du produit")
    features = models.JSONField(default=list, blank=True, help_text="Fonctionnalités principales")
    safety_instructions = models.TextField(blank=True, verbose_name="Consignes de sécurité")
    maintenance_tips = models.TextField(blank=True, verbose_name="Conseils d'entretien")
    warranty_duration = models.IntegerField(default=0, help_text="Durée de garantie en mois")
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)], verbose_name="Prix")
    old_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    discount = models.IntegerField(default=0)
    stock = models.IntegerField(default=0, validators=[MinValueValidator(0)], verbose_name="Stock")
    min_stock_alert = models.IntegerField(default=5, verbose_name="Alerte stock minimum")
    image = models.ImageField(upload_to='products/', null=True, blank=True, verbose_name="Image")
    additional_images = models.JSONField(default=list, blank=True)
    video_url = models.URLField(blank=True, verbose_name="URL de la vidéo de démonstration")
    is_new = models.BooleanField(default=False, verbose_name="Nouveau")
    is_featured = models.BooleanField(default=False, verbose_name="Mis en avant")
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=0)
    rating_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True, verbose_name="Actif")
    thumbnail = models.ImageField(upload_to='products/thumbnails/', null=True, blank=True, verbose_name="Miniature")

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Produit"
        verbose_name_plural = "Produits"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        
        if self.image:
            self.image = resize_image(self.image, 800, 600)
            if not self.thumbnail:
                self.thumbnail = create_thumbnail(self.image)

        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('main:product_detail', args=[self.slug])

    def image_url(self):
        if self.image:
            return self.image.url
        return "https://via.placeholder.com/800x600"

    def thumbnail_url(self):
        if self.thumbnail:
            return self.thumbnail.url
        return "https://via.placeholder.com/200x150"

    def needs_restock(self):
        return self.stock <= self.min_stock_alert

    def get_warranty_display(self):
        if self.warranty_duration == 0:
            return "Pas de garantie"
        elif self.warranty_duration == 12:
            return "1 an"
        else:
            years = self.warranty_duration // 12
            months = self.warranty_duration % 12
            result = []
            if years > 0:
                result.append(f"{years} an{'s' if years > 1 else ''}")
            if months > 0:
                result.append(f"{months} mois")
            return " et ".join(result)

class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews', verbose_name="Produit")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews', verbose_name="Utilisateur")
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)], verbose_name="Note")
    comment = models.TextField(verbose_name="Commentaire")
    pros = models.TextField(blank=True, verbose_name="Points positifs")
    cons = models.TextField(blank=True, verbose_name="Points négatifs")
    usage_duration = models.CharField(max_length=50, blank=True, verbose_name="Durée d'utilisation")
    usage_frequency = models.CharField(max_length=50, blank=True, verbose_name="Fréquence d'utilisation")
    would_recommend = models.BooleanField(default=True, verbose_name="Recommande le produit")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Avis"
        verbose_name_plural = "Avis"
        ordering = ['-created_at']
        unique_together = ['product', 'user']

    def __str__(self):
        return f"Avis de {self.user.username} sur {self.product.name}"

class Inventory(models.Model):
    REASON_CHOICES = [
        ('purchase', 'Achat'),
        ('sale', 'Vente'),
        ('return', 'Retour'),
        ('adjustment', 'Ajustement'),
        ('damage', 'Dommage'),
        ('loss', 'Perte'),
    ]

    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='inventory_records', verbose_name="Produit")
    quantity_changed = models.IntegerField(verbose_name="Quantité modifiée")
    reason = models.CharField(max_length=20, choices=REASON_CHOICES, verbose_name="Raison")
    notes = models.TextField(blank=True, verbose_name="Notes")
    date = models.DateTimeField(auto_now_add=True)
    recorded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name="Enregistré par")
    
    class Meta:
        verbose_name = "Mouvement de stock"
        verbose_name_plural = "Mouvements de stock"
        ordering = ['-date']

    def __str__(self):
        return f"Mouvement de stock pour {self.product.name}: {self.quantity_changed}"

class SupabaseUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    supabase_uid = models.CharField(max_length=255, unique=True)
    phone = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)
    preferences = models.JSONField(default=dict, blank=True)
    newsletter_subscription = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username

class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'En attente'),
        ('confirmed', 'Confirmée'),
        ('preparing', 'En préparation'),
        ('shipped', 'Expédiée'),
        ('delivered', 'Livrée'),
        ('cancelled', 'Annulée'),
    ]

    PAYMENT_STATUS = [
        ('pending', 'En attente'),
        ('paid', 'Payée'),
        ('failed', 'Échouée'),
        ('refunded', 'Remboursée'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(SupabaseUser, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS, default='pending')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    shipping_address = models.TextField()
    shipping_method = models.CharField(max_length=100)
    tracking_number = models.CharField(max_length=100, blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'orders'
        ordering = ['-created_at']

    def __str__(self):
        return f"Commande {self.id} - {self.user.user.username}"

class OrderItem(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product_id = models.UUIDField()
    product_name = models.CharField(max_length=200)
    quantity = models.IntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        db_table = 'order_items'

    def __str__(self):
        return f"{self.quantity}x {self.product_name} dans la commande {self.order.id}"

class Cart(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(SupabaseUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'carts'

    def __str__(self):
        return f"Panier de {self.user.user.username}"

    def get_total(self):
        return sum(item.get_total() for item in self.items.all())

class CartItem(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE)
    product_id = models.UUIDField()
    quantity = models.IntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'cart_items'

    def __str__(self):
        return f"{self.quantity}x Produit {self.product_id} dans le panier {self.cart.id}"

    def get_total(self):
        # Cette méthode devrait récupérer le prix du produit depuis Supabase
        # et le multiplier par la quantité
        return 0  # À implémenter avec l'intégration Supabase
