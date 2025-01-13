from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from main.models.order import Order, OrderItem, Payment
from main.models.base_models import Product, Category, Brand
from unittest.mock import patch
import stripe

User = get_user_model()

class OrderTests(APITestCase):
    def setUp(self):
        # Créer un utilisateur de test
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.client.force_authenticate(user=self.user)

        # Créer une catégorie et une marque
        self.category = Category.objects.create(
            name='Test Category',
            slug='test-category'
        )
        self.brand = Brand.objects.create(
            name='Test Brand',
            slug='test-brand'
        )

        # Créer un produit de test
        self.product = Product.objects.create(
            name='Test Product',
            slug='test-product',
            description='Test Description',
            price=99.99,
            category=self.category,
            brand=self.brand
        )

        # Données de commande de test
        self.order_data = {
            'payment_method': 'card',
            'shipping_address': '123 Test St',
            'billing_address': '123 Test St',
            'items': [
                {
                    'product': self.product.id,
                    'quantity': 2
                }
            ]
        }

    def test_create_order(self):
        """Test de création d'une commande"""
        url = reverse('api:v1:order-list')
        response = self.client.post(url, self.order_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Order.objects.count(), 1)
        self.assertEqual(OrderItem.objects.count(), 1)

    def test_list_orders(self):
        """Test de listage des commandes"""
        # Créer quelques commandes
        Order.objects.create(
            user=self.user,
            payment_method='card',
            shipping_address='123 Test St',
            billing_address='123 Test St',
            subtotal=199.98,
            tax=20.00,
            total=219.98
        )

        url = reverse('api:v1:order-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    @patch('stripe.PaymentIntent.create')
    def test_process_payment(self, mock_payment_intent):
        """Test de traitement d'un paiement"""
        # Créer une commande
        order = Order.objects.create(
            user=self.user,
            payment_method='card',
            shipping_address='123 Test St',
            billing_address='123 Test St',
            subtotal=199.98,
            tax=20.00,
            total=219.98
        )

        # Simuler la réponse de Stripe
        mock_payment_intent.return_value = stripe.PaymentIntent.construct_from({
            'id': 'pi_test123',
            'client_secret': 'test_secret',
            'status': 'requires_payment_method'
        }, 'test_key')

        url = reverse('api:v1:order-process-payment', kwargs={'pk': order.pk})
        response = self.client.post(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('client_secret', response.data)

    @patch('stripe.PaymentIntent.retrieve')
    def test_confirm_payment(self, mock_payment_intent):
        """Test de confirmation d'un paiement"""
        # Créer une commande et un paiement
        order = Order.objects.create(
            user=self.user,
            payment_method='card',
            shipping_address='123 Test St',
            billing_address='123 Test St',
            subtotal=199.98,
            tax=20.00,
            total=219.98
        )
        payment = Payment.objects.create(
            order=order,
            amount=219.98,
            payment_method='card',
            transaction_id='pi_test123'
        )

        # Simuler la réponse de Stripe
        mock_payment_intent.return_value = stripe.PaymentIntent.construct_from({
            'id': 'pi_test123',
            'status': 'succeeded'
        }, 'test_key')

        url = reverse('api:v1:order-confirm-payment', kwargs={'pk': order.pk})
        response = self.client.post(url, {'payment_intent_id': 'pi_test123'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], 'payment_confirmed')

        # Vérifier que le statut de la commande a été mis à jour
        order.refresh_from_db()
        self.assertEqual(order.status, 'paid')

    @patch('stripe.Refund.create')
    def test_refund_payment(self, mock_refund):
        """Test de remboursement"""
        # Créer une commande payée et un paiement
        order = Order.objects.create(
            user=self.user,
            payment_method='card',
            shipping_address='123 Test St',
            billing_address='123 Test St',
            subtotal=199.98,
            tax=20.00,
            total=219.98,
            status='paid'
        )
        payment = Payment.objects.create(
            order=order,
            amount=219.98,
            payment_method='card',
            transaction_id='pi_test123',
            status='completed'
        )

        # Simuler la réponse de Stripe
        mock_refund.return_value = stripe.Refund.construct_from({
            'id': 're_test123',
            'status': 'succeeded'
        }, 'test_key')

        url = reverse('api:v1:payment-refund', kwargs={'pk': payment.pk})
        response = self.client.post(url, {'reason': 'requested_by_customer'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], 'refunded')

        # Vérifier que les statuts ont été mis à jour
        payment.refresh_from_db()
        order.refresh_from_db()
        self.assertEqual(payment.status, 'refunded')
        self.assertEqual(order.status, 'refunded')
