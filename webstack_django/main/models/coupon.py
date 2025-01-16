from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from .base_models import TimestampedModel

class Coupon(TimestampedModel):
    code = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True)
    discount_type = models.CharField(
        max_length=10,
        choices=[
            ('percentage', 'Percentage'),
            ('fixed', 'Fixed Amount')
        ]
    )
    discount_value = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    minimum_order_value = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        default=0
    )
    valid_from = models.DateTimeField()
    valid_until = models.DateTimeField()
    max_uses = models.IntegerField(default=None, null=True, blank=True)
    current_uses = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)

    def is_valid(self, order_total):
        from django.utils import timezone
        now = timezone.now()
        
        if not self.is_active:
            return False, "Coupon is not active"
            
        if now < self.valid_from:
            return False, "Coupon is not yet valid"
            
        if now > self.valid_until:
            return False, "Coupon has expired"
            
        if self.max_uses and self.current_uses >= self.max_uses:
            return False, "Coupon has reached maximum uses"
            
        if order_total < self.minimum_order_value:
            return False, f"Order total must be at least {self.minimum_order_value}"
            
        return True, "Coupon is valid"

    def calculate_discount(self, order_total):
        if self.discount_type == 'percentage':
            return (order_total * self.discount_value) / 100
        return min(self.discount_value, order_total)  # Ne pas dépasser le total

    def use(self):
        self.current_uses += 1
        self.save()
