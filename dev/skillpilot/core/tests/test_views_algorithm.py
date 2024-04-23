import unittest
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User, Group
from core.models import Student, Internship, Recruiter, Company, ComputedMatch

# test algorithm views functions 
class TestViews(TestCase):
    
    # create required data
    def setUp(self):
        self.student = Student.objects.create( # create a student
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
        self.company = Company.objects.create( # create a company
            companyID="C002", 
            companyName="Another Test Company", 
            industrySector="Tech"
        )
        self.recruiter = Recruiter.objects.create( # create a recruiter
            recruiterID="R001", 
            fullName="John Smith", 
            email="john@example.com", 
            companyID=self.company,
            jobTitle="Recruitment Officer"  
        )
        self.internship = Internship.objects.create( # create an internship
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
        self.admin_user = User.objects.create_user(username='admin', password='adminpass')
        admin_group = Group.objects.create(name='Admin')
        self.admin_user.groups.add(admin_group)
        self.admin_user.save()
        self.client.login(username='admin', password='adminpass')


    # Unit tests for algorithm_dashboard view
    def test_algorithm_dashboard_view_get(self):
        url = reverse('algorithm-dashboard')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    # test with no data
    def test_algorithm_dashboard_view_post_no_data(self):
        url = reverse('algorithm-dashboard')
        response = self.client.post(url)
        self.assertEqual(response.status_code, 200)

    # test with data
    def test_algorithm_dashboard_view_post_with_data(self):
        url = reverse('algorithm-dashboard')
        response = self.client.post(url, data={})
        self.assertEqual(response.status_code, 200)

    # test invalid method
    def test_algorithm_dashboard_view_invalid_method(self):
        url = reverse('algorithm-dashboard')
        response = self.client.put(url)
        self.assertEqual(response.status_code, 200)

    #test accessing dashboard with authenticated user
    def test_algorithm_dashboard_view_authenticated_user(self):
        self.client.logout()
        response = self.client.get(reverse('algorithm-dashboard'))
        self.assertRedirects(response, '/home?next=%2Falgorithm-dashboard')
        self.client.login(username='admin', password='adminpass')
        response = self.client.get(reverse('algorithm-dashboard'))
        self.assertEqual(response.status_code, 200)

    # Unit tests for approve_match view
    
    # test approve match function
    def test_approve_match_view_valid_match(self):
        match = ComputedMatch.objects.create(computedMatchID='789', internshipID=self.internship, studentID=self.student)
        url = reverse('approve-match', args=['789'])
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
    """
    def test_approve_match_view_invalid_match(self):
        url = reverse('approve-match', args=['999'])
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
    """
    # Unit tests for reject_match view
    def test_reject_match_view_valid_match(self):
        match = ComputedMatch.objects.create(computedMatchID='789', internshipID=self.internship, studentID=self.student)
        url = reverse('reject-match', args=['789'])
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
    """
    def test_reject_match_view_invalid_match(self):
        url = reverse('reject-match', args=['999'])
        response = self.client.post(url)
        self.assertEqual(response.status_code, 404)
    """
    # Integration tests
    def test_approve_match_integration(self):
        # Ensure match approval correctly updates the database
        match = ComputedMatch.objects.create(computedMatchID='789', internshipID=self.internship, studentID=self.student)
        url = reverse('approve-match', args=['789'])
        self.client.post(url)
        updated_match = ComputedMatch.objects.get(computedMatchID='789')
        self.assertIsNotNone(updated_match.interviewID)
    
    # test match rejection correctly updates the database
    def test_reject_match_integration(self):
        match = ComputedMatch.objects.create(computedMatchID='789', internshipID=self.internship, studentID=self.student)
        url = reverse('reject-match', args=['789'])
        self.client.post(url)
        with self.assertRaises(ComputedMatch.DoesNotExist):
            ComputedMatch.objects.get(computedMatchID='789')

if __name__ == '__main__':
    unittest.main()
