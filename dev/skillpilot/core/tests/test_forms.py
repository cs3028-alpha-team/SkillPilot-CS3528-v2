from django.test import TestCase, Client
from core.models import Student, Internship, Company, Recruiter
from django.contrib.auth.models import User
from django.urls import reverse

#tesing the recruiter dashboard form
class TestRecruiterDashboard(TestCase):
    def setUp(self):
        self.client = Client()

    def test_form_rendering(self):

        recruiter_user = User.objects.create_user(username='tesco', email= 'tesco@fskdgskhdfsjf.com', password='12435687abdn')
        recruiter_user.groups.create(name='Companies') 

        self.client.login(username='tesco', password='12435687abdn')
        
        company = Company.objects.create(
            companyID = 'tesco',
            companyName = 'tesco',
            industrySector = 'retail',
            websiteURL = 'www',
        )
        recruiter = Recruiter.objects.create(
            fullName='tesco',
            recruiterID='tesco4',
            companyID=company,
            jobTitle='tesco LD',
            email='tesco@fskdgskhdfsjf.com',
    
        )
        internship  = Internship.objects.create(
            internshipID = '123',
            companyID=company,
            recruiterID=recruiter,
            contractMode = 'Online',
            contractPattern = 'Full-Time',
            numberPositions = 2,
            field = 'tesco',
            title = 'tesco',
            minGPA = 66,
        )

        form_data = {
            'title': 'tesco',
            'field': 'tesco',
            'contractMode': 'Online',  
            'contractPattern': 'Full-Time',  
            'minGPA': 66,  
            'numberPositions': 2,  
            'recruiterID':recruiter,
            'companyID':company,
        }
        
        response = self.client.post(reverse('recruiter'), data=form_data, follow=True)

        self.assertContains(response, '<form method="POST"')

        self.assertContains(response, '<input type="text" name="title"')
        self.assertContains(response, '<input type="text" name="field"')
        self.assertContains(response, '<input type="text" name="internshipID"')
        self.assertContains(response, '<select name="contractMode"')
        self.assertContains(response, '<select name="contractPattern"')
        self.assertContains(response, '<input type="number" name="minGPA"')
        self.assertContains(response, '<input type="number" name="numberPositions"')

        self.assertContains(response, '<button type="submit"')

#testing the recruiter dashboard 
class TestFormValidation(TestCase):
    def setUp(self):
        self.recruiter_user = User.objects.create_user(username='tesco', email='tesco@fskdgskhdfsjf.com', password='12435687abdn')
        self.recruiter_user.groups.create(name='Companies') 

        self.client.login(username='tesco', password='12435687abdn')
        
    
        self.company = Company.objects.create(
            companyID='tesco',
            companyName='tesco',
            industrySector='retail',
            websiteURL='www',
        )
        
     
        self.recruiter = Recruiter.objects.create(
            fullName='tesco',
            recruiterID='tesco4',
            companyID=self.company,
            jobTitle='tesco LD',
            email='tesco@fskdgskhdfsjf.com',
        )
        
    #testing for missing value appears with an error 
    def test_invalid_input(self):
      
        form_data = {
            'title': '',  #empty value for title 
            'field': 'tesco',
            'contractMode': 'Online',
            'contractPattern': 'Full-Time',
            'minGPA': 66,
            'numberPositions': 2, 
            'recruiterID': 'tesco4',
            'companyID': 'tesco',
        }
        
        response = self.client.post(reverse('recruiter'), data=form_data, follow=True)
        
        self.assertEqual(response.status_code, 200)
        
        form = response.context.get('form')
        self.assertIsNotNone(form)
        
        self.assertFalse(form.is_valid())
        
        self.assertTrue('title' in form.errors)
        self.assertTrue('field' not in form.errors)  
        self.assertTrue('minGPA' not in form.errors)  
    
    #testing valid data posted appears correctly in database 
    def test_valid_input(self):
        form_data2 = {
            'title': 'Interns',
            'field': 'IT',
            'contractMode': 'online',
            'contractPattern': 'FT',
            'minGPA': 70,
            'numberPositions': 5,
            'recruiterID': self.recruiter.pk,
            'companyID': self.company.pk,
            'internshipID': '123',
        }
        
        response = self.client.post(reverse('recruiter'), data=form_data2, follow=True)
        
        self.assertEqual(response.status_code, 200)
        
        form = response.context.get('form')
        
        self.assertTrue(Internship.objects.exists())
        
        saved_internship = Internship.objects.first()
        
        self.assertEqual(saved_internship.title, form_data2['title'])
        self.assertEqual(saved_internship.field, form_data2['field'])
        self.assertEqual(saved_internship.contractMode, form_data2['contractMode'])
        self.assertEqual(saved_internship.contractPattern, form_data2['contractPattern'])
        self.assertEqual(saved_internship.minGPA, form_data2['minGPA'])
        self.assertEqual(saved_internship.numberPositions, form_data2['numberPositions'])
        self.assertEqual(saved_internship.recruiterID.pk, form_data2['recruiterID'])
        self.assertEqual(saved_internship.companyID.pk, form_data2['companyID'])

