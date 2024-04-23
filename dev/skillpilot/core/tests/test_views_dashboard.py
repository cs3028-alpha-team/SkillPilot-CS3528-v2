from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User, Group
from core.models import Student, Interview, Recruiter, Company, Internship
from core.forms import StudentForm

# test student dashboard view
class StudentDashboardViewTest(TestCase):
    
    # create test data
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='test_student', password='password123')
        self.student_group = Group.objects.create(name='Students')
        self.student_group.user_set.add(self.user)

    # test student dashboard with GET request
    def test_student_dashboard_GET(self):
        self.client.login(username='test_student', password='password123')
        response = self.client.get(reverse('student'))
        self.assertEqual(response.status_code, 200)
        #self.assertTemplateUsed(response, 'student_dashboard.html')
    
    # test unauthorised access is redirected
    def test_student_dashboard_not_logged_in(self):
        response = self.client.get(reverse('student'))
        self.assertEqual(response.status_code, 302)  # Redirect to login page

# test recruiter dashboard
class RecruiterDashboardViewTest(TestCase):
    
    # create test data
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='test_recruiter', password='password123')
        self.company_group = Group.objects.create(name='Companies')
        self.company_group.user_set.add(self.user)
        self.company = Company.objects.create(
            companyID="C002", 
            companyName="Another Test Company", 
            industrySector="Tech"
        )
        self.recruiter = Recruiter.objects.create(
            recruiterID="R001", 
            fullName="John Smith", 
            email="bob@example.com", 
            companyID=self.company,
            jobTitle="Recruitment Officer"  
        )

    # test dashboard with GET request
    def test_recruiter_dashboard_GET(self):
        self.client.login(username='test_recruiter', password='password123')
        response = self.client.get(reverse('recruiter'))
        self.assertEqual(response.status_code, 302) # 
        #self.assertTemplateUsed(response, 'recruiter_dashboard.html')

    # test unautherised access is redirected
    def test_recruiter_dashboard_no_logged_in_user(self):
        response = self.client.get(reverse('recruiter'))
        self.assertEqual(response.status_code, 302)  # Redirect to login page

# test update interview function
class UpdateInterviewViewTest(TestCase):
    
    # create test data
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='test_user', password='password123')
        self.student_group = Group.objects.create(name='Students')
        self.student_group.user_set.add(self.user)
        self.company = Company.objects.create(
            companyID="C002", 
            companyName="Another Test Company", 
            industrySector="Tech"
        )
        self.recruiter = Recruiter.objects.create(
            recruiterID="R001", 
            fullName="John Smith", 
            email="bob@example.com", 
            companyID=self.company,
            jobTitle="Recruitment Officer"  
        )
        self.student = Student.objects.create(
            studentID="123", 
            fullName="John Doe", 
            email="john@example.com",
            currProgramme="Computer Science",  
            prevProgramme="None",  
            studyMode=Student.mode.ONLINE, 
            studyPattern=Student.pattern.FULL_TIME,  
            GPA=3.5, 
            desiredContractLength=Student.contractLength.ONE_YEAR,  
            willingRelocate=True,  
            aspirations="To excel in software development"  
        )
        self.internship = Internship.objects.create(
            internshipID="789", 
            title="Test Internship", 
            recruiterID=self.recruiter, 
            companyID=self.company, 
            contractMode=Internship.mode.ONLINE,  
            contractPattern=Internship.pattern.FULL_TIME, 
            numberPositions=5, 
            field='IT', 
            minGPA=3.0
        )
        self.interview = Interview.objects.create(
            interviewID=1,
            companyID=self.company, 
            studentID=self.student, 
            recruiterID=self.recruiter, 
            internshipID=self.internship, 
            outcome='accepted'
        )
    
    # test with POST request
    def test_update_interview_POST(self):
        self.client.login(username='test_user', password='password123')
        response = self.client.post(reverse('update-interview', args=[self.interview.interviewID]), {'new_outcome': 'accepted'})
        self.assertEqual(response.status_code, 302)  

# test integration of views
class ViewIntegrationTest(TestCase):
    
    # create test data
    def setUp(self):
        self.client = Client()
        self.user_recruiter = User.objects.create_user(username='test_recruiter', password='password123')
        self.user_student = User.objects.create_user(username='test_student', password='password123')
        self.company_group = Group.objects.create(name='Companies')
        self.company_group.user_set.add(self.user_recruiter)
        self.student_group = Group.objects.create(name='Students')
        self.student_group.user_set.add(self.user_student)
        self.company = Company.objects.create(
            companyID="C002", 
            companyName="Another Test Company", 
            industrySector="Tech"
        )
        self.recruiter = Recruiter.objects.create(
            recruiterID="R001", 
            fullName="John Smith", 
            email="bob@example.com", 
            companyID=self.company,
            jobTitle="Recruitment Officer"  
        )
        self.student = Student.objects.create(
            studentID="123", 
            fullName="John Doe", 
            email="john@example.com",
            currProgramme="Computer Science",  
            prevProgramme="None",  
            studyMode=Student.mode.ONLINE, 
            studyPattern=Student.pattern.FULL_TIME,  
            GPA=3.5, 
            desiredContractLength=Student.contractLength.ONE_YEAR,  
            willingRelocate=True,  
            aspirations="To excel in software development"  
        )
        self.internship = Internship.objects.create(
            internshipID="789", 
            title="Test Internship", 
            recruiterID=self.recruiter, 
            companyID=self.company, 
            contractMode=Internship.mode.ONLINE,  
            contractPattern=Internship.pattern.FULL_TIME, 
            numberPositions=5, 
            field='IT', 
            minGPA=3.0
        )
        self.interview = Interview.objects.create(
            interviewID=1,
            companyID=self.company, 
            studentID=self.student, 
            recruiterID=self.recruiter, 
            internshipID=self.internship, 
            outcome='accepted'
        )
        
    # test recruiter dashboard integration
    def test_recruiter_dashboard_integration(self):
        # Test recruiter dashboard with GET request
        self.client.login(username='test_recruiter', password='password123')
        response = self.client.get(reverse('recruiter'))
        self.assertEqual(response.status_code, 302) # 
        #self.assertTemplateUsed(response, 'recruiter_dashboard.html')

    # test student dashboard integration
    def test_student_dashboard_integration(self):
        # Test student dashboard with GET request
        self.client.login(username='test_student', password='password123')
        response = self.client.get(reverse('student'))
        self.assertEqual(response.status_code, 200)
        #self.assertTemplateUsed(response, 'student_dashboard.html')

    # test update interview integration
    def test_update_interview_integration(self):
        # Test update interview with POST request
        self.client.login(username='test_student', password='password123')
        response = self.client.post(reverse('update-interview', args=[self.interview.interviewID]), {'new_outcome': 'accepted'})
        self.assertEqual(response.status_code, 302)  # Redirect upon updating the interview