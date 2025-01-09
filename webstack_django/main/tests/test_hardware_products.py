from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from decimal import Decimal
from main.models import Category, Brand, Product, Review, SupabaseUser
from main.supabase_auth import SupabaseAuth
from .utils import with_test_auth
import json
import os

class HardwareProductViewsTest(TestCase):
    def setUp(self):
        # Activation du mode test
        os.environ['TESTING'] = 'True'
        
        # Configuration de Supabase pour les tests
        os.environ['SUPABASE_URL'] = 'https://hbqppveyaofcqtqipp.supabase.co'
        os.environ['SUPABASE_KEY'] = 'test-key'
        
        # Création d'un utilisateur de test
        self.user = User.objects.create_user(
            username='testuser',
            email='bentaifourmoh@gmail.com',
            password='AdminDroguerie2024!'
        )
        self.supabase_user = SupabaseUser.objects.create(
            user=self.user,
            supabase_uid='6742e94f-f8f4-410a-9a5a-6e3f2efb7d55'  # ID réel de Supabase
        )
        
        # Création du client de test et login
        self.client = Client()
        self.client.login(username='testuser', password='AdminDroguerie2024!')
        
        # Configuration de la session avec un faux token pour les tests
        session = self.client.session
        session['supabase_access_token'] = 'fake_test_token'
        session.save()
        
        # Mock de la vérification du token pour les tests
        def mock_verify_token(self, token):
            return True
        SupabaseAuth.verify_token = mock_verify_token
        
        # Création des catégories
        self.categories = {
            'hand_tools': Category.objects.create(
                name='Outils à main',
                category_type='hand_tools'
            ),
            'power_tools': Category.objects.create(
                name='Outils électriques',
                category_type='power_tools'
            )
        }
        
        # Création des marques
        self.brands = {
            'stanley': Brand.objects.create(
                name='Stanley',
                quality_tier='premium'
            ),
            'dewalt': Brand.objects.create(
                name='DeWalt',
                quality_tier='professional'
            )
        }
        
        # Création des produits
        self.products = {
            'hammer': Product.objects.create(
                category=self.categories['hand_tools'],
                brand=self.brands['stanley'],
                name='Marteau de charpentier Stanley',
                description='Marteau robuste pour travaux de charpente',
                price=Decimal('49.99'),
                stock=10,
                power_source='manual',
                usage_type='professional',
                warranty_duration=24
            ),
            'drill': Product.objects.create(
                category=self.categories['power_tools'],
                brand=self.brands['dewalt'],
                name='Perceuse DeWalt 18V',
                description='Perceuse sans fil puissante',
                price=Decimal('299.99'),
                stock=5,
                power_source='battery',
                usage_type='professional',
                warranty_duration=36
            )
        }

    def tearDown(self):
        # Désactivation du mode test
        os.environ['TESTING'] = 'False'

    @with_test_auth
    def test_product_list_view(self):
        response = self.client.get(reverse('main:product_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Marteau de charpentier Stanley')
        self.assertContains(response, 'Perceuse DeWalt 18V')

    @with_test_auth
    def test_product_detail_view(self):
        product = self.products['hammer']
        response = self.client.get(
            reverse('main:product_detail', kwargs={'slug': product.slug})
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, product.name)
        self.assertContains(response, str(product.price))

    @with_test_auth
    def test_category_filter(self):
        response = self.client.get(
            reverse('main:product_list'),
            {'category': self.categories['hand_tools'].category_type}
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Marteau de charpentier Stanley')
        self.assertNotContains(response, 'Perceuse DeWalt 18V')

    @with_test_auth
    def test_brand_filter(self):
        response = self.client.get(
            reverse('main:product_list'),
            {'brand': self.brands['stanley'].name}
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Marteau de charpentier Stanley')
        self.assertNotContains(response, 'Perceuse DeWalt 18V')

    @with_test_auth
    def test_price_filter(self):
        response = self.client.get(
            reverse('main:product_list'),
            {'min_price': '40', 'max_price': '100'}
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Marteau de charpentier Stanley')
        self.assertNotContains(response, 'Perceuse DeWalt 18V')

    @with_test_auth
    def test_usage_type_filter(self):
        response = self.client.get(
            reverse('main:product_list'),
            {'usage_type': 'professional'}
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Marteau de charpentier Stanley')
        self.assertContains(response, 'Perceuse DeWalt 18V')

    @with_test_auth
    def test_power_source_filter(self):
        response = self.client.get(
            reverse('main:product_list'),
            {'power_source': 'manual'}
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Marteau de charpentier Stanley')
        self.assertNotContains(response, 'Perceuse DeWalt 18V')

    @with_test_auth
    def test_warranty_filter(self):
        response = self.client.get(
            reverse('main:product_list'),
            {'min_warranty': '3'}
        )
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, 'Marteau de charpentier Stanley')
        self.assertContains(response, 'Perceuse DeWalt 18V')


class HardwareProductFeaturesTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(
            name='Outils à main',
            category_type='hand_tools'
        )
        self.brand = Brand.objects.create(
            name='Stanley',
            quality_tier='premium',
            warranty_info='Garantie à vie sur les outils à main'
        )
        self.product = Product.objects.create(
            category=self.category,
            brand=self.brand,
            name='Marteau de charpentier',
            description='Marteau professionnel',
            usage_type='professional',
            power_source='manual',
            specifications={
                'poids': '600g',
                'longueur': '330mm'
            },
            features=['Manche ergonomique'],
            warranty_duration=240,
            price=Decimal('49.99'),
            stock=10,
            min_stock_alert=3
        )

    def test_warranty_display(self):
        self.assertEqual(self.product.get_warranty_display(), "20 ans")
        
        self.product.warranty_duration = 18
        self.product.save()
        self.assertEqual(self.product.get_warranty_display(), "1 an et 6 mois")
        
        self.product.warranty_duration = 0
        self.product.save()
        self.assertEqual(self.product.get_warranty_display(), "Pas de garantie")

    def test_stock_alerts(self):
        self.assertFalse(self.product.needs_restock())
        
        self.product.stock = 3
        self.product.save()
        self.assertTrue(self.product.needs_restock())
        
        self.product.stock = 2
        self.product.save()
        self.assertTrue(self.product.needs_restock())

    def test_specifications_validation(self):
        # Test des spécifications valides
        self.product.specifications = {
            'poids': '600g',
            'longueur': '330mm',
            'matériau': 'acier'
        }
        self.product.save()
        self.assertEqual(len(self.product.specifications), 3)

        # Test des spécifications avec valeurs numériques
        self.product.specifications = {
            'poids': 600,
            'longueur': 330
        }
        self.product.save()
        self.assertEqual(len(self.product.specifications), 2)

    def test_features_validation(self):
        # Test des caractéristiques valides
        self.product.features = [
            'Manche ergonomique',
            'Anti-vibrations',
            'Tête forgée'
        ]
        self.product.save()
        self.assertEqual(len(self.product.features), 3)


class HardwareProductSearchTest(TestCase):
    def setUp(self):
        # Activation du mode test
        os.environ['TESTING'] = 'True'
        
        # Configuration de Supabase pour les tests
        os.environ['SUPABASE_URL'] = 'https://hbqppveyaofcqtqipp.supabase.co'
        os.environ['SUPABASE_KEY'] = 'test-key'
        
        # Création d'un utilisateur de test
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.supabase_user = SupabaseUser.objects.create(
            user=self.user,
            supabase_uid='test123'
        )
        
        # Création du client de test et login
        self.client = Client()
        self.client.login(username='testuser', password='testpass123')
        
        # Configuration de la session avec un faux token pour les tests
        session = self.client.session
        session['supabase_access_token'] = 'fake_test_token'
        session.save()
        
        # Mock de la vérification du token pour les tests
        def mock_verify_token(self, token):
            return True
        SupabaseAuth.verify_token = mock_verify_token
        
        # Création des catégories et marques
        self.category = Category.objects.create(
            name='Outils à main',
            category_type='hand_tools'
        )
        self.brand = Brand.objects.create(
            name='Stanley',
            quality_tier='premium'
        )
        
        # Création de produits pour les tests de recherche
        self.products = [
            Product.objects.create(
                category=self.category,
                brand=self.brand,
                name='Marteau de charpentier Stanley',
                description='Parfait pour les travaux de charpente',
                price=Decimal('49.99'),
                stock=10,
                power_source='manual',
                usage_type='professional'
            ),
            Product.objects.create(
                category=self.category,
                brand=self.brand,
                name='Tournevis Stanley',
                description='Idéal pour le bricolage',
                price=Decimal('9.99'),
                stock=20,
                power_source='manual',
                usage_type='diy'
            )
        ]

    def tearDown(self):
        # Désactivation du mode test
        os.environ['TESTING'] = 'False'

    @with_test_auth
    def test_basic_search(self):
        response = self.client.get(
            reverse('main:product_search'),
            {'q': 'marteau'}
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Marteau de charpentier Stanley')
        self.assertNotContains(response, 'Tournevis Stanley')

    @with_test_auth
    def test_advanced_search(self):
        response = self.client.get(
            reverse('main:product_search'),
            {
                'q': 'stanley',
                'category': 'hand_tools',
                'min_price': '40',
                'max_price': '100'
            }
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Marteau de charpentier Stanley')
        self.assertNotContains(response, 'Tournevis Stanley')

    @with_test_auth
    def test_search_by_usage(self):
        response = self.client.get(
            reverse('main:product_search'),
            {'usage_type': 'professional'}
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Marteau de charpentier Stanley')
        self.assertNotContains(response, 'Tournevis Stanley')
