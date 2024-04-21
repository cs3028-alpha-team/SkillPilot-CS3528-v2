from django.test import TestCase, Client
from django.urls import reverse
from core.models import Student, Recruiter, Internship, Company
from django.contrib.auth.models import User

#test student detail view
class TestStudentViews(TestCase):
    def setUp(self):
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
        self.client = Client()
        
        # Create a user and log in
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.client.login(username='testuser', password='12345')

    def test_student_details_view(self):
        response = self.client.get(reverse('student-details', kwargs={'studentID': '123'}))
        self.assertContains(response, self.student.fullName)

    def test_student_details_view_no_student(self):
        response = self.client.get(reverse('student-details', kwargs={'studentID': '999'}))
        self.assertEqual(response.status_code, 302)

#test recruiter detail views
class TestRecruiterViews(TestCase):
    def setUp(self):
        self.company = Company.objects.create(
            companyID="C001", 
            companyName="Test Company", 
            industrySector="Tech"
        )
        self.recruiter = Recruiter.objects.create(
            recruiterID="456", 
            fullName="Jane Doe", 
            email="jane@example.com", 
            companyID=self.company,
            jobTitle="Recruitment Manager"  
        )
        self.client = Client()
        
        # Create a user and log in
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.client.login(username='testuser', password='12345')

    def test_recruiter_details_view(self):
        response = self.client.get(reverse('recruiter-details', kwargs={'recruiterID': '456'}))
        self.assertContains(response, self.recruiter.fullName)

    def test_recruiter_details_view_no_recruiter(self):
        response = self.client.get(reverse('recruiter-details', kwargs={'recruiterID': '999'}))
        self.assertEqual(response.status_code, 302)

#test internship detail views
class TestInternshipViews(TestCase):
    def setUp(self):
        self.company = Company.objects.create(
            companyID="C002", 
            companyName="Another Test Company", 
            industrySector="Tech"
        )
        self.recruiter = Recruiter.objects.create(
            recruiterID="R001", 
            fullName="John Smith", 
            email="john@example.com", 
            companyID=self.company,
            jobTitle="Recruitment Officer"  
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
        self.client = Client()
        
        # Create a user and log in
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.client.login(username='testuser', password='12345')


    def test_internship_details_view(self):
        response = self.client.get(reverse('internship-details', kwargs={'internshipID': '789'}))
        self.assertContains(response, self.internship.title)

    def test_internship_details_view_no_internship(self):
        response = self.client.get(reverse('internship-details', kwargs={'internshipID': '999'}))
        self.assertEqual(response.status_code, 302)
