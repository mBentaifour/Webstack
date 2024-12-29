from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from main.models import Category, Product, Review
from decimal import Decimal

class ProductViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.category = Category.objects.create(
            name='Test Category',
            slug='test-category'
        )
        self.product = Product.objects.create(
            name='Test Product',
            slug='test-product',
            description='Test Description',
            price=Decimal('99.99'),
            stock=10,
            category=self.category
        )
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )

    def test_product_list_view(self):
        response = self.client.get(reverse('main:product_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/product_list.html')
        self.assertContains(response, 'Test Product')

    def test_product_detail_view(self):
        response = self.client.get(
            reverse('main:product_detail', kwargs={'slug': self.product.slug})
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/product_detail.html')
        self.assertContains(response, self.product.name)
        self.assertContains(response, self.product.description)

    def test_category_list_view(self):
        response = self.client.get(reverse('main:category_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/category_list.html')
        self.assertContains(response, 'Test Category')

    def test_category_detail_view(self):
        response = self.client.get(
            reverse('main:category_detail', kwargs={'slug': self.category.slug})
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/category_detail.html')
        self.assertContains(response, self.category.name)
        self.assertContains(response, self.product.name)

class ReviewViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
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
        self.review_data = {
            'rating': 5,
            'comment': 'Great product!'
        }

    def test_add_review_authenticated(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post(
            reverse('main:add_review', kwargs={'product_slug': self.product.slug}),
            self.review_data
        )
        self.assertEqual(response.status_code, 302)  # Redirect after success
        self.assertTrue(
            Review.objects.filter(
                product=self.product,
                user=self.user
            ).exists()
        )

    def test_add_review_unauthenticated(self):
        response = self.client.post(
            reverse('main:add_review', kwargs={'product_slug': self.product.slug}),
            self.review_data
        )
        self.assertEqual(response.status_code, 302)  # Redirect to login
        self.assertFalse(
            Review.objects.filter(
                product=self.product
            ).exists()
        )

class SearchViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.category = Category.objects.create(
            name='Test Category',
            slug='test-category'
        )
        self.product1 = Product.objects.create(
            name='Test Product',
            slug='test-product',
            description='Test Description',
            price=Decimal('99.99'),
            stock=10,
            category=self.category
        )
        self.product2 = Product.objects.create(
            name='Another Product',
            slug='another-product',
            description='Another Description',
            price=Decimal('149.99'),
            stock=5,
            category=self.category
        )

    def test_search_results(self):
        response = self.client.get(reverse('main:search'), {'q': 'Test'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/search_results.html')
        self.assertContains(response, 'Test Product')
        self.assertNotContains(response, 'Another Product')

    def test_empty_search(self):
        response = self.client.get(reverse('main:search'), {'q': ''})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/search_results.html')
        self.assertContains(response, 'Veuillez entrer un terme de recherche')
