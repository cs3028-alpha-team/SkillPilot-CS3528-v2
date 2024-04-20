from django.test import SimpleTestCase, TestCase, Client
from django.urls import reverse, resolve
from core import views

class UrlResolveTestCase(SimpleTestCase):
    def test_home_url_resolves(self):
        url = reverse('home')
        self.assertEquals(resolve(url).func, views.home)

    def test_recruiter_url_resolves(self):
        url = reverse('recruiter')
        self.assertEquals(resolve(url).func, views.recruiter_dashboard)

    def test_admin_page_url_resolves(self):
        url = reverse('admin_page')
        self.assertEquals(resolve(url).func, views.admin)

    def test_contacts_url_resolves(self):
        url = reverse('contacts')
        self.assertEquals(resolve(url).func, views.contacts)

    def test_send_email_url_resolves(self):
        url = reverse('send-email')
        self.assertEquals(resolve(url).func, views.send_email)

    def test_approve_match_url_resolves(self):
        url = reverse('approve-match', args=['test_match_id'])
        self.assertEquals(resolve(url).func, views.approve_match)
    """
    def test_reject_match_url_resolves(self):
        url = reverse('reject-match', args=['invalid_id'])
        self.assertEquals(resolve(url).func, views.reject_match)
    """
    def test_algorithm_dashboard_url_resolves(self):
        url = reverse('algorithm-dashboard')
        self.assertEquals(resolve(url).func, views.algorithm_dashboard)

    def test_student_url_resolves(self):
        url = reverse('student')
        self.assertEquals(resolve(url).func, views.student_dashboard)

    def test_manage_companies_url_resolves(self):
        url = reverse('manage-companies')
        self.assertEquals(resolve(url).func, views.companies_management_tool)

    def test_register_company_url_resolves(self):
        url = reverse('register-company')
        self.assertEquals(resolve(url).func, views.register_company)

    def test_delete_company_url_resolves(self):
        url = reverse('delete-company', args=['test_company_id'])
        self.assertEquals(resolve(url).func, views.delete_company)

    def test_delete_user_url_resolves(self):
        url = reverse('delete-user')
        self.assertEquals(resolve(url).func, views.delete_user)

    def test_delete_recruiter_url_resolves(self):
        url = reverse('delete-recruiter')
        self.assertEquals(resolve(url).func, views.delete_recruiter)

    def test_student_signup_url_resolves(self):
        url = reverse('student-signup')
        self.assertEquals(resolve(url).func, views.student_signup)

    def test_student_login_url_resolves(self):
        url = reverse('student-login')
        self.assertEquals(resolve(url).func, views.student_login)

    def test_admin_login_url_resolves(self):
        url = reverse('admin-login')
        self.assertEquals(resolve(url).func, views.admin_login)

    def test_recruiter_signup_url_resolves(self):
        url = reverse('recruiter-signup')
        self.assertEquals(resolve(url).func, views.recruiter_signup)

    def test_recruiter_login_url_resolves(self):
        url = reverse('recruiter-login')
        self.assertEquals(resolve(url).func, views.recruiter_login)

    def test_logout_url_resolves(self):
        url = reverse('logout')
        self.assertEquals(resolve(url).func, views.user_logout)

    def test_query_students_url_resolves(self):
        url = reverse('query-students')
        self.assertEquals(resolve(url).func, views.query_students)

    def test_query_recruiters_url_resolves(self):
        url = reverse('query-recruiters')
        self.assertEquals(resolve(url).func, views.query_recruiters)

    def test_query_internships_url_resolves(self):
        url = reverse('query-internships')
        self.assertEquals(resolve(url).func, views.query_internships)

    def test_student_details_url_resolves(self):
        url = reverse('student-details', args=['test_student_id'])
        self.assertEquals(resolve(url).func, views.student_details)

    def test_recruiter_details_url_resolves(self):
        url = reverse('recruiter-details', args=['test_recruiter_id'])
        self.assertEquals(resolve(url).func, views.recruiter_details)

    def test_internship_details_url_resolves(self):
        url = reverse('internship-details', args=['test_internship_id'])
        self.assertEquals(resolve(url).func, views.internship_details)

    def test_update_interview_url_resolves(self):
        url = reverse('update-interview', args=[1])  # Assuming interview_id of 1
        self.assertEquals(resolve(url).func, views.update_interview)

class HttpResponseTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def test_home_url(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)

    def test_recruiter_url(self):
        response = self.client.get(reverse('recruiter'))
        self.assertEqual(response.status_code, 302) # redirect

    def test_admin_page_url(self):
        response = self.client.get(reverse('admin_page'))
        self.assertEqual(response.status_code, 302) # redirect

    def test_contacts_url(self):
        response = self.client.get(reverse('contacts'))
        self.assertEqual(response.status_code, 200)

    def test_send_email_url(self):
        response = self.client.get(reverse('send-email'))
        self.assertEqual(response.status_code, 200)

    def test_approve_match_url(self):
        response = self.client.get(reverse('approve-match', args=['invalid_id']))
        self.assertEqual(response.status_code, 302) # redirect
    """
    def test_reject_match_url(self):
        response = self.client.get(reverse('reject-match', args=['invalid_id']))
        self.assertEqual(response.status_code, 302) # redirect
    """
    def test_algorithm_dashboard_url(self):
        response = self.client.get(reverse('algorithm-dashboard'))
        self.assertEqual(response.status_code, 302) # redirect

    def test_student_url(self):
        response = self.client.get(reverse('student'))
        self.assertEqual(response.status_code, 302) # redirect

    def test_manage_companies_url(self):
        response = self.client.get(reverse('manage-companies'))
        self.assertEqual(response.status_code, 302) # redirect

    def test_register_company_url(self):
        response = self.client.get(reverse('register-company'))
        self.assertEqual(response.status_code, 302) # redirect 

    def test_delete_company_url(self):
        response = self.client.get(reverse('delete-company', args=['test_company_id']))
        self.assertEqual(response.status_code, 302) # redirect

    def test_delete_user_url(self):
        response = self.client.get(reverse('delete-user'))
        self.assertEqual(response.status_code, 302) # redirect

    def test_delete_recruiter_url(self):
        response = self.client.get(reverse('delete-recruiter'))
        self.assertEqual(response.status_code, 302) # redirect

    def test_student_signup_url(self):
        response = self.client.get(reverse('student-signup'))
        self.assertEqual(response.status_code, 200)

    def test_student_login_url(self):
        response = self.client.get(reverse('student-login'))
        self.assertEqual(response.status_code, 200)

    def test_admin_login_url(self):
        response = self.client.get(reverse('admin-login'))
        self.assertEqual(response.status_code, 200)

    def test_recruiter_signup_url(self):
        response = self.client.get(reverse('recruiter-signup'))
        self.assertEqual(response.status_code, 200)

    def test_recruiter_login_url(self):
        response = self.client.get(reverse('recruiter-login'))
        self.assertEqual(response.status_code, 200)

    def test_logout_url(self):
        response = self.client.get(reverse('logout'))
        self.assertEqual(response.status_code, 302) # redirect

    def test_query_students_url(self):
        response = self.client.get(reverse('query-students'))
        self.assertEqual(response.status_code, 302) # redirect

    def test_query_recruiters_url(self):
        response = self.client.get(reverse('query-recruiters'))
        self.assertEqual(response.status_code, 302) # redirect

    def test_query_internships_url(self):
        response = self.client.get(reverse('query-internships'))
        self.assertEqual(response.status_code, 302) # redirect

    def test_student_details_url(self):
        response = self.client.get(reverse('student-details', args=['test_student_id']))
        self.assertEqual(response.status_code, 302) # redirect

    def test_recruiter_details_url(self):
        response = self.client.get(reverse('recruiter-details', args=['invalid_id'])) # test redirect for invalid id
        self.assertEqual(response.status_code, 302) # redirect

    def test_internship_details_url(self):
        response = self.client.get(reverse('internship-details', args=['invalid_id']))
        self.assertEqual(response.status_code, 302) # redirect

    def test_update_interview_url(self):
        response = self.client.get(reverse('update-interview', args=[1]))  # Assuming interview_id of 1
        self.assertEqual(response.status_code, 302) # redirect
