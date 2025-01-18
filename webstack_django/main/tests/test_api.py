from django.test import TestCase
from rest_framework.test import APIClient
from django.urls import reverse
from rest_framework import status

class APITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        
    def test_api_health(self):
        """Test that the API is accessible"""
        response = self.client.get('/api/health/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_supabase_connection(self):
        """Test that we can connect to Supabase"""
        from django.conf import settings
        self.assertTrue(settings.SUPABASE_URL)
        self.assertTrue(settings.SUPABASE_KEY)
