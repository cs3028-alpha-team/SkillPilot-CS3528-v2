from django.test import TestCase, Client
from django.urls import reverse
from .models import Company, Recruiter, Internship
from .forms import CompanyRegistrationForm
from django.contrib.auth.models import User

class UnitTests(TestCase):
    def setUp(self):
        self.client = Client()

        # Create test user with Admin role
        self.user = User.objects.create_user(username='test_admin', email='admin@test.com', password='password')
        self.user.is_staff = True
        self.user.save()

        self.company1 = Company.objects.create(companyName="Company1", industrySector="Tech", websiteURL="http://company1.com")
        self.company2 = Company.objects.create(companyName="Company2", industrySector="Finance", websiteURL="http://company2.com")
        self.recruiter = Recruiter.objects.create(companyID=self.company1.companyID, email='recruiter@company1.com')

    def tearDown(self):
        self.user.delete()
        self.company1.delete()
        self.company2.delete()
        self.recruiter.delete()

    def test_delete_company_view(self):
        self.client.force_login(self.user)
        response = self.client.post(reverse('delete-company', kwargs={'companyID': self.company1.companyID}))
        self.assertEqual(response.status_code, 302)  # Redirects after successful deletion

        # Check if company1 is deleted
        self.assertFalse(Company.objects.filter(companyID=self.company1.companyID).exists())
        # Check if associated recruiter is deleted
        self.assertFalse(Recruiter.objects.filter(companyID=self.company1.companyID).exists())
        # Check if associated internships are deleted
        self.assertFalse(Internship.objects.filter(companyID=self.company1.companyID).exists())

        # Attempt to delete non-existent company
        response = self.client.post(reverse('delete-company', kwargs={'companyID': 999}))
        self.assertEqual(response.status_code, 302)  # Redirects

    def test_register_company_view(self):
        self.client.force_login(self.user)
        response = self.client.post(reverse('register-company'), {
            'companyName': 'New Company',
            'companyField': 'Technology',
            'companyWebsite': 'http://newcompany.com',
            'recruiterToken': 'token123'
        })
        self.assertEqual(response.status_code, 302)  # Redirects after successful registration

        # Check if new company is created
        new_company = Company.objects.get(companyName='New Company')
        self.assertEqual(new_company.industrySector, 'Technology')
        self.assertEqual(new_company.websiteURL, 'http://newcompany.com')

class IntegrationTests(TestCase):
    def setUp(self):
        self.client = Client()

        # Create test user with Admin role
        self.user = User.objects.create_user(username='test_admin', email='admin@test.com', password='password')
        self.user.is_staff = True
        self.user.save()

        self.company1 = Company.objects.create(companyName="Company1", industrySector="Tech", websiteURL="http://company1.com")
        self.company2 = Company.objects.create(companyName="Company2", industrySector="Finance", websiteURL="http://company2.com")
        self.recruiter = Recruiter.objects.create(companyID=self.company1.companyID, email='recruiter@company1.com')

    def tearDown(self):
        self.user.delete()
        self.company1.delete()
        self.company2.delete()
        self.recruiter.delete()

    def test_companies_management_tool_view(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('companies-management-tool'))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['companies'], [repr(self.company1), repr(self.company2)])
        
        # Test POST request with filter_condition='claimed'
        response = self.client.post(reverse('companies-management-tool'), {'companyFilterDrowpdown': 'claimed'})
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['companies'], [repr(self.company1)])
        
        # Test POST request with filter_condition='unclaimed'
        response = self.client.post(reverse('companies-management-tool'), {'companyFilterDrowpdown': 'unclaimed'})
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['companies'], [repr(self.company2)])
