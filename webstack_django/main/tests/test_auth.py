from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse

User = get_user_model()

class AuthenticationTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.register_url = reverse('main:api_register')
        self.login_url = reverse('main:api_login')
        self.user_data = {
            'email': 'test@example.com',
            'username': 'testuser',
            'password': 'TestPassword123!',
            'first_name': 'John',
            'last_name': 'Doe',
            'phone_number': '+33612345678'
        }

    def test_user_registration(self):
        """Test l'inscription d'un nouvel utilisateur"""
        response = self.client.post(self.register_url, self.user_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(email=self.user_data['email']).exists())

    def test_user_registration_invalid_data(self):
        """Test l'inscription avec des données invalides"""
        invalid_data = {
            'email': 'invalid-email',
            'password': '123'  # Mot de passe trop court
        }
        response = self.client.post(self.register_url, invalid_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_login(self):
        """Test la connexion d'un utilisateur"""
        # Créer un utilisateur
        User.objects.create_user(
            email=self.user_data['email'],
            username=self.user_data['username'],
            password=self.user_data['password']
        )
        
        # Tenter de se connecter
        response = self.client.post(self.login_url, {
            'email': self.user_data['email'],
            'password': self.user_data['password']
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)

    def test_user_login_wrong_credentials(self):
        """Test la connexion avec de mauvaises informations d'identification"""
        response = self.client.post(self.login_url, {
            'email': 'wrong@example.com',
            'password': 'WrongPassword123!'
        })
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

class UserProfileTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            email='test@example.com',
            username='testuser',
            password='TestPassword123!',
            first_name='John',
            last_name='Doe'
        )
        self.client.force_authenticate(user=self.user)
        self.profile_url = reverse('main:profile')

    def test_get_profile(self):
        """Test la récupération du profil utilisateur"""
        response = self.client.get(self.profile_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email'], self.user.email)

    def test_update_profile(self):
        """Test la mise à jour du profil utilisateur"""
        update_data = {
            'first_name': 'Jane',
            'last_name': 'Smith',
            'phone_number': '+33687654321'
        }
        response = self.client.patch(self.profile_url, update_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, update_data['first_name'])

    def test_change_password(self):
        """Test le changement de mot de passe"""
        change_password_url = reverse('main:change_password')
        data = {
            'old_password': 'TestPassword123!',
            'new_password': 'NewPassword456!',
            'confirm_password': 'NewPassword456!'
        }
        response = self.client.post(change_password_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Vérifier que le nouveau mot de passe fonctionne
        self.assertTrue(
            self.client.login(
                email='test@example.com',
                password='NewPassword456!'
            )
        )
