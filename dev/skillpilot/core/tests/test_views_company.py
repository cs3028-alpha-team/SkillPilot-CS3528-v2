from django.test import TestCase, Client
from django.urls import reverse
from core.models import Company, Recruiter, Internship
from core.forms import CompanyRegistrationForm
from django.contrib.auth.models import User, Group

# Test company view functions
class UnitTests(TestCase):
    def setUp(self):
        self.client = Client()

        # Create test admin user
        self.admin_user = User.objects.create_user(username='admin', email='admin@test.com', password='adminpass')
        admin_group = Group.objects.create(name='Admin')
        self.admin_user.groups.add(admin_group)

        # Create test data
        self.company1 = Company.objects.create(companyID="C001", companyName="Company1", industrySector="Tech", websiteURL="http://company1.com")
        self.company2 = Company.objects.create(companyID="C002", companyName="Company2", industrySector="Finance", websiteURL="http://company2.com")
        self.recruiter = Recruiter.objects.create(recruiterID="R001", fullName="John Smith", companyID=self.company1, email='recruiter@company1.com')

        self.user1 = User.objects.create_user(username='user1', email='user1@test.com', password='password')
        self.user2 = User.objects.create_user(username='user2', email='user2@test.com', password='password')

    def tearDown(self):
        self.admin_user.delete()
        self.user1.delete()
        self.user2.delete()
        self.company1.delete()
        self.company2.delete()
        self.recruiter.delete()

    # Test delete company view
    def test_delete_company_view(self):
        self.client.force_login(self.admin_user)
        response = self.client.post(reverse('delete-company', kwargs={'companyID': self.company1.companyID}))
        self.assertEqual(response.status_code, 302)  # Ensure redirects after successful deletion
        
        # Check if company1 and associated objects are deleted
        self.assertFalse(Company.objects.filter(companyID=self.company1.companyID).exists())
        self.assertFalse(Recruiter.objects.filter(companyID=self.company1.companyID).exists())
        self.assertFalse(Internship.objects.filter(companyID=self.company1.companyID).exists())

    # Test registering a company
    def test_register_company_view(self):
        self.client.force_login(self.admin_user)
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

# Test integration of company functions
class IntegrationTests(TestCase):
    def setUp(self):
        self.client = Client()

        self.admin_user = User.objects.create_user(username='admin', email='admin@test.com', password='password')
        self.admin_user.is_staff = True
        admin_group = Group.objects.create(name='Admin')
        self.admin_user.groups.add(admin_group)
        self.client.force_login(self.admin_user)

        self.user = User.objects.create_user(username='user', email='user@test.com', password='password')
        
        # Create test data
        self.company1 = Company.objects.create(companyID="C001", companyName="Company1", industrySector="Tech", websiteURL="http://company1.com")
        self.company2 = Company.objects.create(companyID="C002", companyName="Company2", industrySector="Finance", websiteURL="http://company2.com")
        self.recruiter = Recruiter.objects.create(recruiterID="R001", fullName="John Smith", companyID=self.company1, email='recruiter@company1.com')

    def tearDown(self):
        self.user.delete()
        self.company1.delete()
        self.company2.delete()
        self.recruiter.delete()

    # Test company management view
    def test_companies_management_tool_view(self):
        self.client.force_login(self.admin_user)
        response = self.client.get(reverse('manage-companies'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('companies', response.context)
        companies = response.context['companies'] 
        if companies is not None: # raise an error if the context is none
            self.assertIn(self.company1, companies)
            self.assertIn(self.company2, companies)
        else:
            self.fail("context 'companies' is None") 
        
    # Test filtering data
    # Test POST request with filter condition='claimed'
    def test_companies_management_tool_filter_claimed(self):    
        response = self.client.post(reverse('manage-companies'), {'companyFilterDrowpdown': 'claimed'})
        self.assertEqual(response.status_code, 200) 
        self.assertTrue('companies' in response.context)  
        companies = response.context.get('companies', [])
        if companies is not None:
            self.assertIn(self.company1, companies)
        else:
            self.fail("Response context 'companies' is None")
            
    # Test POST request with filter condition='unclaimed'
    def test_companies_management_tool_filter_unclaimed(self):     
        response = self.client.post(reverse('manage-companies'), {'companyFilterDrowpdown': 'unclaimed'})
        self.assertEqual(response.status_code, 200)  
        self.assertTrue('companies' in response.context)  
        companies = response.context.get('companies', [])
        if companies is not None:
            self.assertIn(self.company2, companies)
        else:
            self.fail("Response context 'companies' is None")