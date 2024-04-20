import unittest
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Student, Internship

class TestViews(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.client.login(username='testuser', password='12345')
        self.student = Student.objects.create(studentID='123', prevProgramme='Test Programme', GPA=3.5, studyMode='Full-time', studyPattern='Regular')
        self.internship = Internship.objects.create(internshipID='456', field='Test Field', minGPA=3.0, contractMode='Full-time', contractPattern='Regular', numberPositions=2)

    # Unit tests for algorithm_dashboard view
    def test_algorithm_dashboard_view_get(self):
        url = reverse('algorithm-dashboard')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_algorithm_dashboard_view_post_no_data(self):
        url = reverse('algorithm-dashboard')
        response = self.client.post(url)
        self.assertEqual(response.status_code, 200)

    def test_algorithm_dashboard_view_post_with_data(self):
        url = reverse('algorithm-dashboard')
        response = self.client.post(url, data={})
        self.assertEqual(response.status_code, 200)

    def test_algorithm_dashboard_view_invalid_method(self):
        url = reverse('algorithm-dashboard')
        response = self.client.put(url)
        self.assertEqual(response.status_code, 405)

    def test_algorithm_dashboard_view_authenticated_user(self):
        self.client.logout()
        response = self.client.get(reverse('algorithm-dashboard'))
        self.assertRedirects(response, '/login/?next=/algorithm-dashboard/')
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('algorithm-dashboard'))
        self.assertEqual(response.status_code, 200)

    # Unit tests for approve_match view
    def test_approve_match_view_valid_match(self):
        match = ComputedMatch.objects.create(computedMatchID='789', internshipID=self.internship, studentID=self.student)
        url = reverse('approve-match', args=['789'])
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)

    def test_approve_match_view_invalid_match(self):
        url = reverse('approve-match', args=['999'])
        response = self.client.post(url)
        self.assertEqual(response.status_code, 404)

    # Unit tests for reject_match view
    def test_reject_match_view_valid_match(self):
        match = ComputedMatch.objects.create(computedMatchID='789', internshipID=self.internship, studentID=self.student)
        url = reverse('reject-match', args=['789'])
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)

    def test_reject_match_view_invalid_match(self):
        url = reverse('reject-match', args=['999'])
        response = self.client.post(url)
        self.assertEqual(response.status_code, 404)

    # Integration tests
    def test_approve_match_integration(self):
        # Ensure match approval correctly updates the database
        match = ComputedMatch.objects.create(computedMatchID='789', internshipID=self.internship, studentID=self.student)
        url = reverse('approve-match', args=['789'])
        self.client.post(url)
        updated_match = ComputedMatch.objects.get(computedMatchID='789')
        self.assertIsNotNone(updated_match.interviewID)

    def test_reject_match_integration(self):
        # Ensure match rejection correctly updates the database
        match = ComputedMatch.objects.create(computedMatchID='789', internshipID=self.internship, studentID=self.student)
        url = reverse('reject-match', args=['789'])
        self.client.post(url)
        with self.assertRaises(ComputedMatch.DoesNotExist):
            ComputedMatch.objects.get(computedMatchID='789')

if __name__ == '__main__':
    unittest.main()
