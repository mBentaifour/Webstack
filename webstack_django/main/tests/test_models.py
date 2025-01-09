from django.test import TestCase
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.utils import timezone
from decimal import Decimal
from main.models import (
    Category, Brand, Product, Review, 
    Inventory, SupabaseUser, Order, OrderItem
)

class CategoryModelTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(
            name="Outils à main",
            category_type="hand_tools",
            description="Tous les outils manuels pour l'artisanat",
            icon="fas fa-hammer",
            tips=["Nettoyer après usage", "Ranger dans un endroit sec"]
        )

    def test_category_creation(self):
        self.assertEqual(self.category.name, "Outils à main")
        self.assertEqual(self.category.category_type, "hand_tools")
        self.assertTrue(self.category.slug)
        self.assertEqual(len(self.category.tips), 2)

class BrandModelTest(TestCase):
    def setUp(self):
        self.brand = Brand.objects.create(
            name="Stanley",
            quality_tier="premium",
            country_of_origin="États-Unis",
            warranty_info="Garantie à vie sur les outils à main"
        )

    def test_brand_creation(self):
        self.assertEqual(self.brand.name, "Stanley")
        self.assertEqual(self.brand.quality_tier, "premium")
        self.assertTrue(self.brand.slug)

class ProductModelTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(
            name="Outils électriques",
            category_type="power_tools"
        )
        self.brand = Brand.objects.create(
            name="DeWalt",
            quality_tier="professional"
        )
        self.product = Product.objects.create(
            category=self.category,
            brand=self.brand,
            name="Perceuse sans fil 18V",
            description="Perceuse professionnelle avec batterie Li-ion",
            usage_type="professional",
            power_source="battery",
            specifications={
                "voltage": "18V",
                "batterie": "Li-ion 4.0Ah",
                "vitesse": "0-1500 tr/min"
            },
            features=["Mandrin auto-serrant", "LED de travail", "2 batteries incluses"],
            safety_instructions="Porter des lunettes de protection. Tenir hors de portée des enfants.",
            maintenance_tips="Nettoyer après chaque utilisation. Recharger les batteries régulièrement.",
            warranty_duration=24,
            price=Decimal("299.99"),
            stock=10,
            min_stock_alert=3
        )

    def test_product_creation(self):
        self.assertEqual(self.product.name, "Perceuse sans fil 18V")
        self.assertEqual(self.product.warranty_duration, 24)
        self.assertEqual(self.product.get_warranty_display(), "2 ans")
        self.assertFalse(self.product.needs_restock())

    def test_stock_alert(self):
        self.product.stock = 2
        self.product.save()
        self.assertTrue(self.product.needs_restock())

class ReviewModelTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name="Outils à main")
        self.product = Product.objects.create(
            category=self.category,
            name="Marteau de charpentier",
            price=Decimal("29.99"),
            stock=5
        )
        self.user = User.objects.create_user(
            username="client1",
            password="testpass123"
        )
        self.review = Review.objects.create(
            product=self.product,
            user=self.user,
            rating=5,
            comment="Excellent outil",
            pros="Robuste, bonne prise en main",
            cons="Un peu lourd",
            usage_duration="6 mois",
            usage_frequency="Quotidienne",
            would_recommend=True
        )

    def test_review_creation(self):
        self.assertEqual(self.review.rating, 5)
        self.assertTrue(self.review.would_recommend)
        self.assertEqual(self.review.usage_frequency, "Quotidienne")

class InventoryModelTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name="Outils à main")
        self.product = Product.objects.create(
            category=self.category,
            name="Tournevis cruciforme",
            price=Decimal("9.99"),
            stock=20
        )
        self.user = User.objects.create_user(
            username="gestionnaire",
            password="testpass123"
        )
        self.inventory = Inventory.objects.create(
            product=self.product,
            quantity_changed=-5,
            reason="sale",
            notes="Vente en magasin",
            recorded_by=self.user
        )

    def test_inventory_movement(self):
        self.assertEqual(self.inventory.quantity_changed, -5)
        self.assertEqual(self.inventory.reason, "sale")
        self.assertTrue(self.inventory.recorded_by)

class OrderModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="client2",
            password="testpass123"
        )
        self.supabase_user = SupabaseUser.objects.create(
            user=self.user,
            supabase_uid="test123",
            phone="+33612345678",
            address="123 Rue du Commerce, Paris"
        )
        self.category = Category.objects.create(name="Outils à main")
        self.product = Product.objects.create(
            category=self.category,
            name="Scie à métaux",
            price=Decimal("24.99"),
            stock=15
        )
        self.order = Order.objects.create(
            user=self.supabase_user,
            status="confirmed",
            payment_status="paid",
            total_amount=Decimal("24.99"),
            shipping_address="123 Rue du Commerce, Paris",
            shipping_method="Colissimo",
            tracking_number="1234567890"
        )
        self.order_item = OrderItem.objects.create(
            order=self.order,
            product_id=self.product.id,
            product_name=self.product.name,
            quantity=1,
            unit_price=self.product.price,
            total_price=self.product.price
        )

    def test_order_creation(self):
        self.assertEqual(self.order.status, "confirmed")
        self.assertEqual(self.order.payment_status, "paid")
        self.assertEqual(self.order_item.quantity, 1)
        self.assertEqual(self.order_item.total_price, Decimal("24.99"))
