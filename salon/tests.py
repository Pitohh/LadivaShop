from rest_framework.test import APITestCase
from rest_framework import status
from account.models import User
from salon.models import Client
from django.test import TestCase
from django.urls import reverse
from salon.models import Appointment, Sale, Client, Product, Service
from datetime import date, timedelta

class DashboardViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.login(username='testuser', password='testpass')
        self.url = reverse('dashboard')

        # Créer des données de test
        client = Client.objects.create(nom="Test Client", email="test@test.com", telephone="1234567890")
        product = Product.objects.create(nom="Test Product", quantite=5, prix=100.00)
        service = Service.objects.create(nom="Test Service", prix=50.00, duree="01:00:00")

        Appointment.objects.create(client=client, service=service, date=date.today(), heure="12:00:00")
        Sale.objects.create(total=150.00, moyen_paiement="cash")

    def test_dashboard_view_context(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertIn('username', response.context)
        self.assertIn('appointments', response.context)
        self.assertIn('sales', response.context)
        self.assertIn('clients', response.context)
        self.assertIn('low_stock_products', response.context)
        
class ClientViewSetTest(APITestCase):
    def setUp(self):
        # Créer un utilisateur admin
        self.admin = User.objects.create_user(
            username="admin", email="admin@test.com", password="adminpass", role="admin"
        )
        # Créer un client existant
        self.client_user = Client.objects.create(
            nom="John Doe", email="johndoe@test.com", telephone="1234567890"
        )
        self.url = "/api/clients/"  # Correspond à l'URL définie dans urls.py

    def test_list_clients_as_admin(self):
        self.client.login(username="admin", password="adminpass")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_client_as_admin(self):
        self.client.login(username="admin", password="adminpass")
        data = {"nom": "Jane Doe", "email": "janedoe@test.com", "telephone": "9876543210"}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_list_clients_as_unauthenticated_user(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
