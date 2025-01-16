from django.db import models
from django.conf import settings
from .base_models import TimestampedModel, Product

class Wishlist(TimestampedModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='wishlists')
    products = models.ManyToManyField(Product, through='WishlistItem')

    class Meta:
        ordering = ['-created_at']

class WishlistItem(TimestampedModel):
    wishlist = models.ForeignKey(Wishlist, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    
    class Meta:
        unique_together = ('wishlist', 'product')
