from django.test import TestCase, override_settings
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from main.models.base_models import Product, Category
from main.models.order import Order, OrderItem
from decimal import Decimal
import stripe
from django.conf import settings

User = get_user_model()

@override_settings(STRIPE_SECRET_KEY='sk_test_51OgJRXGtJYfWxHxvZVMIHNYDfvvpOJKYXPKXBPHZBRDXmGWDXPWPVZFVZFVZFVZF')
class OrderTests(TestCase):
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
        
        # Créer des produits
        self.product1 = Product.objects.create(
            name='Smartphone',
            slug='smartphone',
            description='A test smartphone',
            price=Decimal('499.99'),
            stock=50,
            category=self.category
        )
        
        self.product2 = Product.objects.create(
            name='Laptop',
            slug='laptop',
            description='A test laptop',
            price=Decimal('999.99'),
            stock=30,
            category=self.category
        )

    def test_create_order(self):
        """Test la création d'une commande"""
        data = {
            'items': [
                {'product': self.product1.id, 'quantity': 2},
                {'product': self.product2.id, 'quantity': 1}
            ]
        }
        
        response = self.client.post(reverse('main:order-list'), data)
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        order = Order.objects.get(id=response.data['id'])
        self.assertEqual(order.user, self.user)
        self.assertEqual(order.items.count(), 2)
        
        # Vérifier les calculs
        expected_subtotal = (self.product1.price * 2) + self.product2.price
        expected_tax = expected_subtotal * Decimal('0.20')  # TVA 20%
        expected_shipping = Decimal('0')  # Gratuit car > 50€
        expected_total = expected_subtotal + expected_tax + expected_shipping
        
        self.assertEqual(order.subtotal, expected_subtotal)
        self.assertEqual(order.tax, expected_tax)
        self.assertEqual(order.shipping_cost, expected_shipping)
        self.assertEqual(order.total, expected_total)

    def test_order_with_insufficient_stock(self):
        """Test la création d'une commande avec stock insuffisant"""
        data = {
            'items': [
                {'product': self.product1.id, 'quantity': 51}  # Stock est de 50
            ]
        }
        
        response = self.client.post(reverse('main:order-list'), data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_order_payment_process(self):
        """Test le processus de paiement d'une commande"""
        # Créer une commande
        order = Order.objects.create(
            user=self.user,
            subtotal=Decimal('100.00'),
            tax=Decimal('20.00'),
            shipping_cost=Decimal('0'),
            total=Decimal('120.00')
        )
        OrderItem.objects.create(
            order=order,
            product=self.product1,
            quantity=1,
            unit_price=self.product1.price,
            total_price=self.product1.price
        )
        
        # Initier le paiement
        response = self.client.post(
            reverse('main:order-process-payment', kwargs={'pk': order.id})
        )
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('client_secret', response.data)
        self.assertIn('payment_id', response.data)

    def test_order_confirmation(self):
        """Test la confirmation de commande"""
        order = Order.objects.create(
            user=self.user,
            subtotal=Decimal('100.00'),
            tax=Decimal('20.00'),
            shipping_cost=Decimal('0'),
            total=Decimal('120.00')
        )
        
        # Simuler un paiement réussi
        payment_intent = stripe.PaymentIntent.create(
            amount=12000,  # En centimes
            currency='eur'
        )
        
        response = self.client.post(
            reverse('main:order-confirm-payment', kwargs={'pk': order.id}),
            {'payment_intent_id': payment_intent.id}
        )
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        order.refresh_from_db()
        self.assertEqual(order.status, 'paid')

    def test_order_history(self):
        """Test l'historique des commandes"""
        # Créer quelques commandes
        for i in range(3):
            order = Order.objects.create(
                user=self.user,
                subtotal=Decimal('100.00'),
                tax=Decimal('20.00'),
                shipping_cost=Decimal('0'),
                total=Decimal('120.00')
            )
            OrderItem.objects.create(
                order=order,
                product=self.product1,
                quantity=1,
                unit_price=self.product1.price,
                total_price=self.product1.price
            )
        
        response = self.client.get(reverse('main:order-list'))
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)

    def test_order_detail(self):
        """Test les détails d'une commande"""
        order = Order.objects.create(
            user=self.user,
            subtotal=Decimal('100.00'),
            tax=Decimal('20.00'),
            shipping_cost=Decimal('0'),
            total=Decimal('120.00')
        )
        OrderItem.objects.create(
            order=order,
            product=self.product1,
            quantity=1,
            unit_price=self.product1.price,
            total_price=self.product1.price
        )
        
        response = self.client.get(
            reverse('main:order-detail', kwargs={'pk': order.id})
        )
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], order.id)
        self.assertEqual(len(response.data['items']), 1)

    def test_shipping_cost_calculation(self):
        """Test le calcul des frais de livraison"""
        # Commande < 50€ (frais de livraison de 5.99€)
        data = {
            'items': [
                {'product': self.product1.id, 'quantity': 1}
            ]
        }
        response = self.client.post(reverse('main:order-list'), data)
        order = Order.objects.get(id=response.data['id'])
        self.assertEqual(order.shipping_cost, Decimal('5.99'))
        
        # Commande > 50€ (livraison gratuite)
        data = {
            'items': [
                {'product': self.product2.id, 'quantity': 1}  # 999.99€
            ]
        }
        response = self.client.post(reverse('main:order-list'), data)
        order = Order.objects.get(id=response.data['id'])
        self.assertEqual(order.shipping_cost, Decimal('0'))
