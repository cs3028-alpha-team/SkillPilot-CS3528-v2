from django.test import TestCase, Client
from django.contrib.auth.models import User, Group
from core.models import Student, Recruiter, Company
from django.urls import reverse
import logging

class DeleteUserTestCase(TestCase):
    
    def setUp(self):
        self.client = Client() 

        # Create a test user
        self.user = User.objects.create_user(username='teststudent', email='student@example.com', password='testpassword')
        self.group = Group.objects.create(name='Students')
        self.user.groups.add(self.group)

        self.student = Student.objects.create(
            studentID="123", 
            fullName="John Doe", 
            email="student@example.com",
            currProgramme="Computer Science",  
            prevProgramme="None",  
            studyMode=Student.mode.ONLINE, 
            studyPattern=Student.pattern.FULL_TIME,  
            GPA=3.5, 
            desiredContractLength=Student.contractLength.ONE_YEAR,  
            willingRelocate=True,  
            aspirations="To excel in software development"  
        )

        self.client.login(email='student@example.com', password='testpassword')

        # Configure logging
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)
        self.handler = logging.StreamHandler()
        self.handler.setLevel(logging.DEBUG)
        self.logger.addHandler(self.handler)

    def tearDown(self):
        self.handler.close()
        
    def test_invalid_method_delete_user(self):
        # Log a debug message
        self.logger.debug("Starting test_invalid_method_delete_user")
        
        url = reverse('delete-user')    # use GET to go to url

        response = self.client.get(url)  
        self.assertEqual(response.status_code, 405)  
        self.assertTrue(User.objects.filter(email='student@example.com').exists())

    def test_valid_delete_user(self):
        # Log a debug message
        self.logger.debug("Starting test_valid_delete_user")
        
        url = reverse('delete-user')
        response = self.client.post(url) 
        self.assertEqual(response.status_code, 302)
        self.assertFalse(User.objects.filter(email='student@example.com').exists())

class DeleteRecruiterTestCase(TestCase):
    
    def setUp(self):
        self.client = Client() 

        self.user = User.objects.create_user(username='testcompany', email='company@example.com', password='testpassword')
        self.group = Group.objects.create(name='Companies')
        self.user.groups.add(self.group)

        self.company = Company.objects.create(
            companyID="C002", 
            companyName="Another Test Company", 
            industrySector="Tech"
        )

        self.recruiter = Recruiter.objects.create(
            recruiterID="R001", 
            fullName="John Smith", 
            email="recruiter@example.com", 
            companyID=self.company,
            jobTitle="Recruitment Officer"  
        )

        self.client.login(email='company@example.com', password='testpassword')

        # Configure logging
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)
        self.handler = logging.StreamHandler()
        self.handler.setLevel(logging.DEBUG)
        self.logger.addHandler(self.handler)

    def tearDown(self):
        self.handler.close()

    def test_invalid_method_delete_recruiter(self):
        # Log a debug message
        self.logger.debug("Starting test_invalid_method_delete_recruiter")
        
        url = reverse('delete-recruiter')
        response = self.client.get(url) 
        self.assertEqual(response.status_code, 405)  
        self.assertTrue(User.objects.filter(email='company@example.com').exists())

    def test_valid_delete_recruiter(self):
        # Log a debug message
        self.logger.debug("Starting test_valid_delete_recruiter")
        
        url = reverse('delete-recruiter')
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        self.assertFalse(User.objects.filter(email='company@example.com').exists())
        self.assertFalse(Recruiter.objects.filter(user=self.user).exists())
