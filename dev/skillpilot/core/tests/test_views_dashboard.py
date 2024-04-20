from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User, Group
from .models import Student, Interview, Recruiter
from .forms import StudentForm

class StudentDashboardViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='test_student', password='password123')
        self.student_group = Group.objects.create(name='Students')
        self.student_group.user_set.add(self.user)

    def test_student_dashboard_GET(self):
        self.client.login(username='test_student', password='password123')
        response = self.client.get(reverse('student'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'student_dashboard.html')

    def test_student_dashboard_not_logged_in(self):
        response = self.client.get(reverse('student'))
        self.assertEqual(response.status_code, 302)  # Redirect to login page

class RecruiterDashboardViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='test_recruiter', password='password123')
        self.company_group = Group.objects.create(name='Companies')
        self.company_group.user_set.add(self.user)
        self.recruiter = Recruiter.objects.create(email='test_recruiter@example.com')

    def test_recruiter_dashboard_GET(self):
        self.client.login(username='test_recruiter', password='password123')
        response = self.client.get(reverse('recruiter'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'recruiter_dashboard.html')

    def test_recruiter_dashboard_no_logged_in_user(self):
        response = self.client.get(reverse('recruiter'))
        self.assertEqual(response.status_code, 302)  # Redirect to login page

class UpdateInterviewViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='test_user', password='password123')
        self.student_group = Group.objects.create(name='Students')
        self.student_group.user_set.add(self.user)
        self.interview = Interview.objects.create(interviewID=1)
    
    def test_update_interview_POST(self):
        self.client.login(username='test_user', password='password123')
        response = self.client.post(reverse('update_interview', args=[self.interview.interviewID]), {'new_outcome': 'accepted'})
        self.assertEqual(response.status_code, 302)  # Redirect upon updating the interview
        
class ViewIntegrationTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user_recruiter = User.objects.create_user(username='test_recruiter', password='password123')
        self.user_student = User.objects.create_user(username='test_student', password='password123')
        self.company_group = Group.objects.create(name='Companies')
        self.company_group.user_set.add(self.user_recruiter)
        self.student_group = Group.objects.create(name='Students')
        self.student_group.user_set.add(self.user_student)
        self.recruiter = Recruiter.objects.create(email='test_recruiter@example.com')
        self.interview = Interview.objects.create(interviewID=1)
        self.student = Student.objects.create(email='test_student@example.com')

    def test_recruiter_dashboard_integration(self):
        # Test recruiter dashboard with GET request
        self.client.login(username='test_recruiter', password='password123')
        response = self.client.get(reverse('recruiter'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'recruiter_dashboard.html')

        # Test recruiter dashboard without logging in (unauthorized access)
        response = self.client.get(reverse('recruiter'))
        self.assertEqual(response.status_code, 302)  # Redirect to login page

    def test_student_dashboard_integration(self):
        # Test student dashboard with GET request
        self.client.login(username='test_student', password='password123')
        response = self.client.get(reverse('student'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'student_dashboard.html')

        # Test student dashboard without logging in (unauthorized access)
        response = self.client.get(reverse('student'))
        self.assertEqual(response.status_code, 302)  # Redirect to login page

    def test_update_interview_integration(self):
        # Test update interview with POST request
        self.client.login(username='test_student', password='password123')
        response = self.client.post(reverse('update_interview', args=[self.interview.interviewID]), {'new_outcome': 'accepted'})
        self.assertEqual(response.status_code, 302)  # Redirect upon updating the interview