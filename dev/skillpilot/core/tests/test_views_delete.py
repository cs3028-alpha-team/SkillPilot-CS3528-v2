from core.views import delete_user, delete_recruiter
from django.test import TestCase, Client
from django.contrib.auth.models import User, Group
from core.models import Student, Recruiter, Internship, Company

# test delete user views
class DeleteUserTestCase(TestCase):
    
    # create test data and test user
    def setUp(self):
        self.client = Client() # create user
        self.user = User.objects.create_user(username='teststudent', email='student@example.com', password='testpassword')
        self.group, _ = Group.objects.get_or_create(name='Students')
        self.user.groups.add(self.group)
        self.client.login(email='student@example.com', password='testpassword')

        self.student = Student.objects.create( # create student
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

    # test delete user
    def test_valid_delete_user(self):
        response = self.client.post('/delete_user/')
        self.assertEqual(response.status_code, 302)
        self.assertFalse(User.objects.filter(email='student@example.com').exists())
    
    # test delete user with an invalid method
    def test_invalid_method_delete_user(self):
        response = self.client.get('/delete_user/')
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(email='student@example.com').exists())

# test delete recruiter
class DeleteRecruiterTestCase(TestCase):
    
    # create test data and user
    def setUp(self):
        self.client = Client() # create test user
        self.user = User.objects.create_user(username='testcompany', email='company@example.com', password='testpassword')
        self.group, _ = Group.objects.get_or_create(name='Companies')
        self.user.groups.add(self.group)
        self.client.login(email='company@example.com', password='testpassword')
        
        self.company = Company.objects.create( # create test company
            companyID="C002", 
            companyName="Another Test Company", 
            industrySector="Tech"
        )
        self.recruiter = Recruiter.objects.create( # create test recruiter
            recruiterID="R001", 
            fullName="John Smith", 
            email="recruiter@example.com", 
            companyID=self.company,
            jobTitle="Recruitment Officer"  
        )

    # test delete recruiter
    def test_valid_delete_recruiter(self):
        response = self.client.post('/delete_recruiter/')
        self.assertEqual(response.status_code, 302)
        self.assertFalse(User.objects.filter(email='company@example.com').exists())
        self.assertFalse(Recruiter.objects.filter(user=self.user).exists())

    # test delete with student account
    def test_invalid_no_recruiter(self):
        # create test student and login
        self.user.username = 'teststudent'
        self.user.email = 'student@example.com'
        self.user.save()
        self.group, _ = Group.objects.get_or_create(name='Students')
        self.user.groups.add(self.group)
        self.client.login(email='student@example.com', password='testpassword')

        # try to delete a recruiter
        response = self.client.post('/delete_recruiter/')
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(email='student@example.com').exists())

    # test delete recruiter with invalid method
    def test_invalid_method_delete_recruiter(self):
        response = self.client.get('/delete_recruiter/')
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(email='company@example.com').exists())
