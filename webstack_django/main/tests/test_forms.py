from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from main.models import Category, Product
from main.forms import ProductForm, ReviewForm

class ProductFormTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(
            name='Test Category',
            slug='test-category'
        )
        self.valid_data = {
            'name': 'Test Product',
            'description': 'Test Description',
            'price': '99.99',
            'stock': 10,
            'category': self.category.id,
            'is_active': True
        }

    def test_valid_form(self):
        form = ProductForm(data=self.valid_data)
        self.assertTrue(form.is_valid())

    def test_invalid_price(self):
        data = self.valid_data.copy()
        data['price'] = '-10.00'
        form = ProductForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('price', form.errors)

    def test_invalid_stock(self):
        data = self.valid_data.copy()
        data['stock'] = -1
        form = ProductForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('stock', form.errors)

    def test_missing_required_fields(self):
        form = ProductForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 4)  # name, description, price, category

class ReviewFormTest(TestCase):
    def setUp(self):
        self.valid_data = {
            'rating': 5,
            'comment': 'Great product!'
        }

    def test_valid_form(self):
        form = ReviewForm(data=self.valid_data)
        self.assertTrue(form.is_valid())

    def test_invalid_rating(self):
        data = self.valid_data.copy()
        data['rating'] = 6
        form = ReviewForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('rating', form.errors)

    def test_missing_rating(self):
        data = self.valid_data.copy()
        del data['rating']
        form = ReviewForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('rating', form.errors)

    def test_empty_comment(self):
        data = self.valid_data.copy()
        data['comment'] = ''
        form = ReviewForm(data=data)
        self.assertTrue(form.is_valid())  # Comment is optional
