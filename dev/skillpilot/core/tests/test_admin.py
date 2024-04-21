from django.contrib import admin
from django.test import TestCase, Client
from core.models import Student, Internship, Company, Recruiter, Interview, ComputedMatch, SuperUser
from django.contrib.auth.models import User

#test admin page model registrations
class AdminTests(TestCase):
    def test_student_registered(self):
        self.assertIn(Student, admin.site._registry)


    def test_internship_registered(self):
        self.assertIn(Internship, admin.site._registry)


    def test_company_registered(self):
        self.assertIn(Company, admin.site._registry)


    def test_recruiter_registered(self):
        self.assertIn(Recruiter, admin.site._registry)


    def test_interview_registered(self):
        self.assertIn(Interview, admin.site._registry)


    def test_computedmatch_registered(self):
        self.assertIn(ComputedMatch, admin.site._registry)


    def test_superuser_registered(self):
        self.assertIn(SuperUser, admin.site._registry)

#integration testing for django admin 
class AdminIntegrationTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_superuser('admin', 'admin@example.com', 'password')
        self.client = Client()

    def test_admin_page(self):
        logged_in = self.client.login(username='admin', password='password')
        self.assertTrue(logged_in)

        response = self.client.get('/admin/')

        self.assertEqual(response.status_code, 200)

        expected_models = ['Student', 'Internship', 'Company', 'Recruiter', 'Interview', 'Computed match', 'Super user']
        registered_models = []
        for app_data in response.context['available_apps']:
            for model_data in app_data['models']:
                registered_models.append(model_data['name'])
        for model in expected_models:
            plural_model = model + 's'
            self.assertIn(plural_model, registered_models)
