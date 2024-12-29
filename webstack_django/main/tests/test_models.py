from django.test import TestCase
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
from django.core.files.uploadedfile import SimpleUploadedFile
from main.models import Category, Brand, Product, Review, Inventory
from decimal import Decimal

class CategoryModelTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(
            name='Test Category',
            slug='test-category',
            description='Test Description'
        )

    def test_category_creation(self):
        self.assertEqual(self.category.name, 'Test Category')
        self.assertEqual(self.category.slug, 'test-category')
        self.assertEqual(str(self.category), 'Test Category')

    def test_unique_name(self):
        with self.assertRaises(IntegrityError):
            Category.objects.create(
                name='Test Category',
                slug='test-category-2'
            )

class BrandModelTest(TestCase):
    def setUp(self):
        self.brand = Brand.objects.create(
            name='Test Brand',
            description='Test Description',
            website='https://example.com'
        )

    def test_brand_creation(self):
        self.assertEqual(self.brand.name, 'Test Brand')
        self.assertEqual(str(self.brand), 'Test Brand')

    def test_unique_name(self):
        with self.assertRaises(IntegrityError):
            Brand.objects.create(name='Test Brand')

class ProductModelTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(
            name='Test Category',
            slug='test-category'
        )
        self.brand = Brand.objects.create(name='Test Brand')
        self.product = Product.objects.create(
            name='Test Product',
            slug='test-product',
            description='Test Description',
            price=Decimal('99.99'),
            stock=10,
            category=self.category,
            brand=self.brand
        )

    def test_product_creation(self):
        self.assertEqual(self.product.name, 'Test Product')
        self.assertEqual(self.product.price, Decimal('99.99'))
        self.assertEqual(self.product.stock, 10)
        self.assertEqual(str(self.product), 'Test Product')

    def test_negative_price(self):
        with self.assertRaises(ValidationError):
            self.product.price = Decimal('-10.00')
            self.product.full_clean()

    def test_negative_stock(self):
        with self.assertRaises(ValidationError):
            self.product.stock = -1
            self.product.full_clean()

class ReviewModelTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(
            name='Test Category',
            slug='test-category'
        )
        self.product = Product.objects.create(
            name='Test Product',
            slug='test-product',
            price=Decimal('99.99'),
            stock=10,
            category=self.category
        )
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.review = Review.objects.create(
            product=self.product,
            user=self.user,
            rating=5,
            comment='Great product!'
        )

    def test_review_creation(self):
        self.assertEqual(self.review.rating, 5)
        self.assertEqual(self.review.comment, 'Great product!')
        self.assertEqual(
            str(self.review),
            f'Avis de {self.user.username} sur {self.product.name}'
        )

    def test_invalid_rating(self):
        with self.assertRaises(ValidationError):
            self.review.rating = 6
            self.review.full_clean()

    def test_unique_user_product_review(self):
        with self.assertRaises(IntegrityError):
            Review.objects.create(
                product=self.product,
                user=self.user,
                rating=4,
                comment='Another review'
            )

class InventoryModelTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(
            name='Test Category',
            slug='test-category'
        )
        self.product = Product.objects.create(
            name='Test Product',
            slug='test-product',
            price=Decimal('99.99'),
            stock=10,
            category=self.category
        )
        self.inventory = Inventory.objects.create(
            product=self.product,
            quantity_changed=5,
            reason='Stock addition'
        )

    def test_inventory_creation(self):
        self.assertEqual(self.inventory.quantity_changed, 5)
        self.assertEqual(self.inventory.reason, 'Stock addition')
        self.assertEqual(
            str(self.inventory),
            f'Mouvement de stock pour {self.product.name}: 5'
        )
