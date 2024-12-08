from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from contacts.models import Contact

class AccountsViewTest(TestCase):

    def setUp(self):
        """Set up a test client, user, and contact inquiry for testing."""
        self.client = Client()
        
        # Create a test user
        self.user = User.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='password123',
            first_name='Test',
            last_name='User'
        )

        # Create a contact inquiry for the user
        self.contact = Contact.objects.create(
            user_id=self.user.id,
            car_id=1,
            car_title='Test Car',
            create_date='2024-12-01',
            message='Interested in this car'
        )

    def test_login_view_valid_credentials(self):
        """Test the login view with valid credentials."""
        response = self.client.post(reverse('login'), {
            'username': 'testuser',
            'password': 'password123'
        })
        self.assertEqual(response.status_code, 302)  # Redirect to dashboard
        self.assertRedirects(response, reverse('dashboard'))

    def test_login_view_invalid_credentials(self):
        """Test the login view with invalid credentials."""
        response = self.client.post(reverse('login'), {
            'username': 'testuser',
            'password': 'wrongpassword'
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Invalid login credentials')

    def test_register_view_success(self):
        """Test the register view with valid data."""
        response = self.client.post(reverse('register'), {
            'firstname': 'John',
            'lastname': 'Doe',
            'username': 'johndoe',
            'email': 'johndoe@example.com',
            'password': 'password123',
            'confirm_password': 'password123'
        })
        self.assertEqual(response.status_code, 302)  # Redirect to dashboard
        self.assertTrue(User.objects.filter(username='johndoe').exists())

    def test_register_view_password_mismatch(self):
        """Test the register view when passwords do not match."""
        response = self.client.post(reverse('register'), {
            'firstname': 'John',
            'lastname': 'Doe',
            'username': 'johndoe',
            'email': 'johndoe@example.com',
            'password': 'password123',
            'confirm_password': 'password456'
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Passwords do not match')

    def test_register_view_duplicate_username(self):
        """Test the register view with an existing username."""
        response = self.client.post(reverse('register'), {
            'firstname': 'Test',
            'lastname': 'User',
            'username': 'testuser',  # Duplicate username
            'email': 'newemail@example.com',
            'password': 'password123',
            'confirm_password': 'password123'
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Username already exists!')

    def test_register_view_duplicate_email(self):
        """Test the register view with an existing email."""
        response = self.client.post(reverse('register'), {
            'firstname': 'John',
            'lastname': 'Doe',
            'username': 'newusername',
            'email': 'testuser@example.com',  # Duplicate email
            'password': 'password123',
            'confirm_password': 'password123'
        })
    
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Email already exists!')

    def test_dashboard_view_authenticated_user(self):
        """Test the dashboard view with an authenticated user."""
        self.client.login(username='testuser', password='password123')
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Interested in this car')

    def test_dashboard_view_unauthenticated_user(self):
        """Test the dashboard view with an unauthenticated user."""
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 302)  # Redirect to login
        self.assertRedirects(response, f"{reverse('login')}?next={reverse('dashboard')}")

    def test_logout_view(self):
        """Test the logout view."""
        self.client.login(username='testuser', password='password123')
        response = self.client.post(reverse('logout'))
        self.assertEqual(response.status_code, 302)  # Redirect to home
        self.assertRedirects(response, reverse('home'))

    def test_login_required_dashboard_redirect(self):
        """Test that unauthenticated users are redirected from the dashboard."""
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith(reverse('login')))
