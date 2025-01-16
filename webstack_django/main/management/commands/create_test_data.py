from django.core.management.base import BaseCommand
from main.models import Category, Product
from decimal import Decimal

class Command(BaseCommand):
    help = 'Creates test data for the application'

    def handle(self, *args, **kwargs):
        # Create categories
        electronics = Category.objects.create(
            name='Electronics',
            slug='electronics',
            description='Electronic devices and gadgets'
        )
        
        clothing = Category.objects.create(
            name='Clothing',
            slug='clothing',
            description='Fashion and apparel'
        )

        # Create products
        Product.objects.create(
            name='Smartphone',
            slug='smartphone',
            description='Latest model smartphone',
            price=Decimal('699.99'),
            category=electronics,
            stock=50
        )

        Product.objects.create(
            name='Laptop',
            slug='laptop',
            description='High-performance laptop',
            price=Decimal('1299.99'),
            category=electronics,
            stock=30
        )

        Product.objects.create(
            name='T-Shirt',
            slug='t-shirt',
            description='Cotton t-shirt',
            price=Decimal('19.99'),
            category=clothing,
            stock=100
        )

        Product.objects.create(
            name='Jeans',
            slug='jeans',
            description='Classic blue jeans',
            price=Decimal('49.99'),
            category=clothing,
            stock=75
        )

        self.stdout.write(self.style.SUCCESS('Successfully created test data'))
