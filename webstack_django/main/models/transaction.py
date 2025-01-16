from django.db import models
from django.contrib.auth import get_user_model
from decimal import Decimal

User = get_user_model()

class Transaction(models.Model):
    PENDING = 'pending'
    COMPLETED = 'completed'
    FAILED = 'failed'
    REFUNDED = 'refunded'
    
    STATUS_CHOICES = [
        (PENDING, 'En attente'),
        (COMPLETED, 'Complétée'),
        (FAILED, 'Échouée'),
        (REFUNDED, 'Remboursée'),
    ]

    transaction_id = models.CharField(max_length=100, unique=True)
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name='transactions')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=PENDING)
    payment_method = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Informations de facturation
    billing_name = models.CharField(max_length=100)
    billing_address = models.TextField()
    billing_city = models.CharField(max_length=100)
    billing_country = models.CharField(max_length=100)
    billing_postal_code = models.CharField(max_length=20)
    
    # Métadonnées de la transaction
    metadata = models.JSONField(default=dict, blank=True)
    
    class Meta:
        ordering = ['-created_at']
        
    def __str__(self):
        return f"Transaction {self.transaction_id} - {self.amount}€ - {self.status}"
        
    def mark_as_completed(self):
        self.status = self.COMPLETED
        self.save()
        
    def mark_as_failed(self):
        self.status = self.FAILED
        self.save()
        
    def mark_as_refunded(self):
        self.status = self.REFUNDED
        self.save()
