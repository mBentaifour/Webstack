from django.test import TestCase, Client
from django.urls import reverse
import json
from unittest.mock import patch

class AuthAppTests(TestCase):
    def setUp(self):
        # Create a test client
        self.client = Client()
        self.signup_url = reverse('signup')
        self.signin_url = reverse('signin')
        self.check_email_url = reverse('checkEmail')
        self.google_oauth_url = reverse('signin')

        # Example data
        self.valid_user_data = {
            "name": "kasem",
            "email": "kamsdonga@gmail.com",
            "password": "password123",
            "confirmPassword": "password123",
            "language": "en",
            "country": "US",
            "mobilePhone": "1234567890",
            "address1": "123 Main St",
            "address2": "Apt 4",
            "termsAgreed": True
        }

    @patch("auth_.views.supabase.auth.sign_up")
    def test_signup_successful(self, mock_sign_up):
        # Mock Supabase response
        mock_sign_up.return_value = type('obj', (object,), {
            "session": type('obj', (object,), {"access_token": "mock_token"})
        })
        
        response = self.client.post(self.signup_url, json.dumps(self.valid_user_data), content_type='application/json')
        self.assertEqual(response.status_code, 201)
        self.assertIn("User created successfully", response.json()['message'])

    def test_signup_missing_fields(self):
        invalid_data = self.valid_user_data.copy()
        invalid_data.pop("email")
        response = self.client.post(self.signup_url, json.dumps(invalid_data), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertIn("error", response.json())

    @patch("auth_.views.supabase.auth.sign_in_with_password")
    def test_signin_successful(self, mock_sign_in):
        mock_sign_in.return_value = type('obj', (object,), {
            "session": type('obj', (object,), {"access_token": "mock_token"})
        })

        data = {"email": "kamsdonga@gmail.com", "password": "password123"}
        response = self.client.post(self.signin_url, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertIn("Login successful", response.json()['message'])

    def test_signin_invalid_method(self):
        response = self.client.get(self.signin_url)
        self.assertEqual(response.status_code, 405)
        self.assertIn("Only POST requests are allowed", response.json()['error'])

    def test_check_email_format_invalid(self):
        invalid_email_data = {"email": "invalid-email"}
        response = self.client.post(self.check_email_url, json.dumps(invalid_email_data), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertIn("Invalid email format", response.json()['error'])

    @patch("auth_.views.email_exists")
    def test_check_email_exists(self, mock_email_exists):
        mock_email_exists.return_value = True
        valid_email_data = {"email": "test@example.com"}
        response = self.client.post(self.check_email_url, json.dumps(valid_email_data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json()['exists'])

    def test_google_oauth_redirect(self):
        response = self.client.get(self.google_oauth_url)
        self.assertEqual(response.status_code, 302)  # Redirect status
        self.assertIn("google", response.url)

