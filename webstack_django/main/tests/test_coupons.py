from django.test import TestCase
from django.utils import timezone
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from main.models.base_models import Product, Category
from main.models.order import Order, OrderItem
from main.models.coupon import Coupon
from decimal import Decimal
import datetime

User = get_user_model()

class CouponTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        
        # Créer un utilisateur
        self.user = User.objects.create_user(
            email='test@example.com',
            username='testuser',
            password='TestPassword123!'
        )
        self.client.force_authenticate(user=self.user)
        
        # Créer une catégorie
        self.category = Category.objects.create(
            name='Electronics',
            slug='electronics'
        )
        
        # Créer un produit
        self.product = Product.objects.create(
            name='Smartphone',
            slug='smartphone',
            description='A test smartphone',
            price=Decimal('499.99'),
            stock=50,
            category=self.category
        )
        
        # Créer différents types de coupons
        self.create_test_coupons()

    def create_test_coupons(self):
        """Crée différents types de coupons pour les tests"""
        # Coupon classique (réduction fixe)
        self.fixed_coupon = Coupon.objects.create(
            code='FIXED20',
            discount_type='fixed',
            discount_value=20,
            valid_from=timezone.now(),
            valid_until=timezone.now() + datetime.timedelta(days=30),
            min_purchase_amount=100
        )
        
        # Coupon pourcentage
        self.percent_coupon = Coupon.objects.create(
            code='PERCENT10',
            discount_type='percentage',
            discount_value=10,
            valid_from=timezone.now(),
            valid_until=timezone.now() + datetime.timedelta(days=30),
            max_discount_amount=50
        )
        
        # Coupon première commande
        self.first_order_coupon = Coupon.objects.create(
            code='FIRST30',
            discount_type='percentage',
            discount_value=30,
            valid_from=timezone.now(),
            valid_until=timezone.now() + datetime.timedelta(days=30),
            first_order_only=True
        )
        
        # Coupon catégorie spécifique
        self.category_coupon = Coupon.objects.create(
            code='TECH15',
            discount_type='percentage',
            discount_value=15,
            valid_from=timezone.now(),
            valid_until=timezone.now() + datetime.timedelta(days=30)
        )
        self.category_coupon.categories.add(self.category)

    def test_apply_fixed_coupon(self):
        """Test l'application d'un coupon à montant fixe"""
        order = Order.objects.create(
            user=self.user,
            total=Decimal('150.00')
        )
        OrderItem.objects.create(
            order=order,
            product=self.product,
            quantity=1,
            unit_price=self.product.price
        )
        
        response = self.client.post(
            reverse('main:apply_coupon'),
            {'order_id': order.id, 'coupon_code': 'FIXED20'}
        )
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        order.refresh_from_db()
        self.assertEqual(order.discount_amount, Decimal('20.00'))

    def test_apply_percentage_coupon(self):
        """Test l'application d'un coupon pourcentage"""
        order = Order.objects.create(
            user=self.user,
            total=Decimal('200.00')
        )
        OrderItem.objects.create(
            order=order,
            product=self.product,
            quantity=1,
            unit_price=self.product.price
        )
        
        response = self.client.post(
            reverse('main:apply_coupon'),
            {'order_id': order.id, 'coupon_code': 'PERCENT10'}
        )
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        order.refresh_from_db()
        self.assertEqual(order.discount_amount, Decimal('20.00'))

    def test_first_order_coupon(self):
        """Test l'application d'un coupon première commande"""
        # Première commande
        order1 = Order.objects.create(
            user=self.user,
            total=Decimal('100.00')
        )
        
        response = self.client.post(
            reverse('main:apply_coupon'),
            {'order_id': order1.id, 'coupon_code': 'FIRST30'}
        )
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Deuxième commande
        order2 = Order.objects.create(
            user=self.user,
            total=Decimal('100.00')
        )
        
        response = self.client.post(
            reverse('main:apply_coupon'),
            {'order_id': order2.id, 'coupon_code': 'FIRST30'}
        )
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_category_specific_coupon(self):
        """Test l'application d'un coupon spécifique à une catégorie"""
        order = Order.objects.create(
            user=self.user,
            total=Decimal('100.00')
        )
        OrderItem.objects.create(
            order=order,
            product=self.product,  # Produit de la catégorie Electronics
            quantity=1,
            unit_price=self.product.price
        )
        
        response = self.client.post(
            reverse('main:apply_coupon'),
            {'order_id': order.id, 'coupon_code': 'TECH15'}
        )
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_expired_coupon(self):
        """Test l'application d'un coupon expiré"""
        expired_coupon = Coupon.objects.create(
            code='EXPIRED',
            discount_type='fixed',
            discount_value=10,
            valid_from=timezone.now() - datetime.timedelta(days=60),
            valid_until=timezone.now() - datetime.timedelta(days=30)
        )
        
        order = Order.objects.create(
            user=self.user,
            total=Decimal('100.00')
        )
        
        response = self.client.post(
            reverse('main:apply_coupon'),
            {'order_id': order.id, 'coupon_code': 'EXPIRED'}
        )
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_minimum_purchase_requirement(self):
        """Test l'application d'un coupon avec montant minimum d'achat"""
        # Commande inférieure au minimum requis
        order = Order.objects.create(
            user=self.user,
            total=Decimal('90.00')
        )
        
        response = self.client.post(
            reverse('main:apply_coupon'),
            {'order_id': order.id, 'coupon_code': 'FIXED20'}
        )
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
