from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from .base_models import TimestampedModel, Product

class Review(TimestampedModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    title = models.CharField(max_length=100)
    comment = models.TextField()
    is_verified_purchase = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['-created_at']
        unique_together = ('user', 'product')  # Un seul avis par utilisateur par produit

    def save(self, *args, **kwargs):
        # Vérifier si l'utilisateur a acheté le produit
        from .order import Order
        has_purchased = Order.objects.filter(
            user=self.user,
            items__product=self.product,
            status='delivered'
        ).exists()
        self.is_verified_purchase = has_purchased
        super().save(*args, **kwargs)
