from django.test import TestCase, Client
from django.urls import reverse
from .models import Student, Recruiter, Internship, Company
from django.contrib.messages import get_messages
from django.test import TestCase, Client
from django.urls import reverse

class TestStudentViews(TestCase):

    def setUp(self):
        self.student = Student.objects.create(studentID="123", name="John Doe", email="john@example.com")
        self.client = Client()

    def test_student_details_view(self):
        response = self.client.get(reverse('student_details', kwargs={'studentID': '123'}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'student_details.html')
        self.assertEqual(response.context['student'], self.student)

    def test_student_details_view_no_student(self):
        response = self.client.get(reverse('student_details', kwargs={'studentID': '999'}))
        self.assertEqual(response.status_code, 302)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Looks like no student with that ID exists!')

class TestRecruiterViews(TestCase):

    def setUp(self):
        self.company = Company.objects.create(companyName="Test Company")
        self.recruiter = Recruiter.objects.create(recruiterID="456", fullName="Jane Doe", email="jane@example.com", companyID=self.company)
        self.client = Client()

    def test_recruiter_details_view(self):
        response = self.client.get(reverse('recruiter_details', kwargs={'recruiterID': '456'}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'recruiter_details.html')
        self.assertEqual(response.context['recruiter'], self.recruiter)
        self.assertEqual(response.context['company'], self.company.companyName)

    def test_recruiter_details_view_no_recruiter(self):
        response = self.client.get(reverse('recruiter_details', kwargs={'recruiterID': '999'}))
        self.assertEqual(response.status_code, 302)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Looks like no recruiter with that ID exists!')

class TestInternshipViews(TestCase):

    def setUp(self):
        self.company = Company.objects.create(companyName="Test Company")
        self.recruiter = Recruiter.objects.create(fullName="John Smith", email="john@example.com", companyID=self.company)
        self.internship = Internship.objects.create(internshipID="789", title="Test Internship", recruiterID=self.recruiter, companyID=self.company)
        self.client = Client()

    def test_internship_details_view(self):
        response = self.client.get(reverse('internship_details', kwargs={'internshipID': '789'}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'internship_details.html')
        self.assertEqual(response.context['internship'], self.internship)
        self.assertEqual(response.context['recruiter'], self.recruiter.fullName)
        self.assertEqual(response.context['company'], self.company.companyName)

    def test_internship_details_view_no_internship(self):
        response = self.client.get(reverse('internship_details', kwargs={'internshipID': '999'}))
        self.assertEqual(response.status_code, 302)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Looks like no internship with that ID exists!')

class TestIntegration(TestCase):

    def setUp(self):
        self.client = Client()

    def test_student_details_integration(self):
        response = self.client.get(reverse('student_details', kwargs={'studentID': '123'}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'student_details.html')

    def test_recruiter_details_integration(self):
        response = self.client.get(reverse('recruiter_details', kwargs={'recruiterID': '456'}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'recruiter_details.html')

    def test_internship_details_integration(self):
        response = self.client.get(reverse('internship_details', kwargs={'internshipID': '789'}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'internship_details.html')
