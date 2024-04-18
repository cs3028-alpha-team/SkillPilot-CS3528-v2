# Import necessary modules for testing
from django.test import TestCase, Client
from django.contrib.auth.models import User
from .models import Student, Recruiter, Internship

# Import views to be tested
from .views import delete_user, delete_recruiter

class DeleteUserTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', email='test@example.com', password='testpassword')
        self.student = Student.objects.create(user=self.user)
        self.client.login(email='test@example.com', password='testpassword')

    def test_valid_delete_user(self):
        response = self.client.post('/delete_user/')
        self.assertEqual(response.status_code, 302)
        self.assertFalse(User.objects.filter(email='test@example.com').exists())

    def test_invalid_method_delete_user(self):
        response = self.client.get('/delete_user/')
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(email='test@example.com').exists())

class DeleteRecruiterTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testrecruiter', email='recruiter@example.com', password='testpassword')
        self.recruiter = Recruiter.objects.create(user=self.user)
        self.client.login(email='recruiter@example.com', password='testpassword')

    def test_valid_delete_recruiter(self):
        response = self.client.post('/delete_recruiter/')
        self.assertEqual(response.status_code, 302)
        self.assertFalse(User.objects.filter(email='recruiter@example.com').exists())
        self.assertFalse(Recruiter.objects.filter(user=self.user).exists())

    def test_invalid_no_recruiter(self):
        # Logging in as a student, who doesn't have a recruiter associated
        self.user.username = 'teststudent'
        self.user.email = 'student@example.com'
        self.user.save()
        self.client.login(email='student@example.com', password='testpassword')

        response = self.client.post('/delete_recruiter/')
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(email='student@example.com').exists())

    def test_invalid_method_delete_recruiter(self):
        response = self.client.get('/delete_recruiter/')
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(email='recruiter@example.com').exists())
