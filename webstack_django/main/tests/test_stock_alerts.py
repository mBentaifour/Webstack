from django.test import TestCase
from django.core import mail
from django.contrib.auth.models import User
from decimal import Decimal
from main.models import Category, Brand, Product, Inventory, SupabaseUser
from main.stock_alerts import (
    check_low_stock,
    send_stock_alert,
    process_stock_movement,
    generate_stock_report
)
from .test_settings import test_settings, override_settings

@override_settings(**test_settings)
class StockAlertsTest(TestCase):
    def setUp(self):
        # Création des utilisateurs
        self.admin_user = User.objects.create_user(
            username='admin',
            email='admin@example.com',
            password='adminpass123',
            is_staff=True
        )
        self.supabase_user = SupabaseUser.objects.create(
            user=self.admin_user,
            supabase_uid='admin123'
        )

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
                name='Marteau de charpentier',
                price=Decimal('49.99'),
                stock=2,
                min_stock_alert=5
            ),
            'drill': Product.objects.create(
                category=self.categories['power_tools'],
                brand=self.brands['dewalt'],
                name='Perceuse sans fil 18V',
                price=Decimal('299.99'),
                stock=1,
                min_stock_alert=3
            ),
            'screwdriver': Product.objects.create(
                category=self.categories['hand_tools'],
                brand=self.brands['stanley'],
                name='Tournevis cruciforme',
                price=Decimal('9.99'),
                stock=20,
                min_stock_alert=5
            )
        }

    def test_check_low_stock(self):
        low_stock_products = check_low_stock()
        self.assertEqual(len(low_stock_products), 2)
        self.assertIn(self.products['hammer'], low_stock_products)
        self.assertIn(self.products['drill'], low_stock_products)
        self.assertNotIn(self.products['screwdriver'], low_stock_products)

    def test_send_stock_alert(self):
        product = self.products['hammer']
        send_stock_alert(product)
        
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(
            mail.outbox[0].subject,
            f'Alerte stock bas - {product.name}'
        )
        self.assertIn(str(product.stock), mail.outbox[0].body)
        self.assertIn(str(product.min_stock_alert), mail.outbox[0].body)

    def test_process_stock_movement(self):
        product = self.products['hammer']
        initial_stock = product.stock
        
        # Test d'ajout de stock
        movement = process_stock_movement(
            product=product,
            quantity=5,
            reason='purchase',
            notes='Réapprovisionnement',
            user=self.admin_user
        )
        
        product.refresh_from_db()
        self.assertEqual(product.stock, initial_stock + 5)
        self.assertEqual(movement.quantity_changed, 5)
        self.assertEqual(movement.reason, 'purchase')
        
        # Test de retrait de stock
        movement = process_stock_movement(
            product=product,
            quantity=-2,
            reason='sale',
            notes='Vente en magasin',
            user=self.admin_user
        )
        
        product.refresh_from_db()
        self.assertEqual(product.stock, initial_stock + 3)
        self.assertEqual(movement.quantity_changed, -2)
        self.assertEqual(movement.reason, 'sale')

    def test_generate_stock_report(self):
        """Test la génération d'un rapport de stock."""
        # Création de mouvements de stock
        process_stock_movement(
            product=self.products['hammer'],
            quantity=5,
            reason='purchase',
            notes='Réapprovisionnement',
            user=self.admin_user
        )
        process_stock_movement(
            product=self.products['drill'],
            quantity=-1,
            reason='sale',
            notes='Vente',
            user=self.admin_user
        )
        
        report = generate_stock_report()
        
        # Vérification du rapport
        self.assertIn('Produits en stock bas', report['summary']['alerts'])
        self.assertIn('Mouvements de stock récents', report['summary']['alerts'])
        self.assertEqual(len(report['low_stock']), 1)  # Seulement la perceuse
        self.assertEqual(len(report['movements']), 2)
        
        # Vérification des détails du rapport
        drill_data = next(p for p in report['low_stock'] if p['name'] == 'Perceuse sans fil 18V')
        self.assertEqual(drill_data['stock'], 0)
        self.assertEqual(drill_data['min_stock_alert'], 3)

@override_settings(**test_settings)
class CategoryStockAlertsTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(
            name='Outils à main',
            category_type='hand_tools'
        )
        self.brand = Brand.objects.create(
            name='Stanley',
            quality_tier='premium'
        )
        
        # Création de plusieurs produits dans la même catégorie
        self.products = []
        for i in range(5):
            self.products.append(
                Product.objects.create(
                    category=self.category,
                    brand=self.brand,
                    name=f'Outil {i+1}',
                    price=Decimal('19.99'),
                    stock=i,  # 0, 1, 2, 3, 4
                    min_stock_alert=3
                )
            )

    def test_category_stock_status(self):
        low_stock_products = check_low_stock(category=self.category)
        self.assertEqual(len(low_stock_products), 3)  # Les 3 premiers produits

    def test_category_stock_report(self):
        report = generate_stock_report(category=self.category)
        self.assertEqual(len(report['low_stock']), 3)
        self.assertEqual(
            report['summary']['total_products'],
            5
        )
        self.assertEqual(
            report['summary']['low_stock_count'],
            3
        )

@override_settings(**test_settings)
class BrandStockAlertsTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(
            name='Outils à main',
            category_type='hand_tools'
        )
        self.brand = Brand.objects.create(
            name='Stanley',
            quality_tier='premium'
        )
        
        # Création de produits avec différents niveaux de stock
        self.products = {
            'normal': Product.objects.create(
                category=self.category,
                brand=self.brand,
                name='Produit stock normal',
                price=Decimal('19.99'),
                stock=10,
                min_stock_alert=5
            ),
            'low': Product.objects.create(
                category=self.category,
                brand=self.brand,
                name='Produit stock bas',
                price=Decimal('29.99'),
                stock=2,
                min_stock_alert=5
            ),
            'out': Product.objects.create(
                category=self.category,
                brand=self.brand,
                name='Produit rupture stock',
                price=Decimal('39.99'),
                stock=0,
                min_stock_alert=5
            )
        }

    def test_brand_stock_status(self):
        low_stock_products = check_low_stock(brand=self.brand)
        self.assertEqual(len(low_stock_products), 2)  # 'low' et 'out'

    def test_brand_stock_report(self):
        report = generate_stock_report(brand=self.brand)
        self.assertEqual(len(report['low_stock']), 2)
        self.assertEqual(
            report['summary']['total_products'],
            3
        )
        self.assertEqual(
            report['summary']['out_of_stock_count'],
            1
        )
