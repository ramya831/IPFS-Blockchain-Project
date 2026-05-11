from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Transaction

class BlockchainTestCases(TestCase):

    def setUp(self):
        # Create test client
        self.client = Client()

        # Create test user
        self.user = User.objects.create_user(
            username="testuser",
            password="testpass123"
        )

    # 1️⃣ Register User Test
    def test_user_registration(self):
        response = self.client.post('/register/', {
            'username': 'newuser',
            'password1': 'StrongPass123',
            'password2': 'StrongPass123'
        })
        self.assertEqual(response.status_code, 302)  # redirect after success

    # 2️⃣ Login Success Test
    def test_login_success(self):
        login = self.client.login(
            username="testuser",
            password="testpass123"
        )
        self.assertTrue(login)

    # 3️⃣ Login Fail Test
    def test_login_fail(self):
        login = self.client.login(
            username="testuser",
            password="wrongpass"
        )
        self.assertFalse(login)

    # 4️⃣ Add Transaction Test
    def test_add_transaction(self):
        self.client.login(username="testuser", password="testpass123")

        response = self.client.post(
            reverse('add_transaction'),
            {
                'sender': 'Alice',
                'receiver': 'Bob',
                'amount': 500
            }
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Transaction.objects.count(), 1)

    # 5️⃣ View Transactions Test
    def test_view_transactions(self):
        self.client.login(username="testuser", password="testpass123")

        Transaction.objects.create(
            sender="Alice",
            receiver="Bob",
            amount=200
        )

        
