from django.test import SimpleTestCase
from django.urls import reverse, resolve
from core import views

# test that the view obtained by 'reversing' the url given 
# in each step corresponds to the expected one 
class TestUrls(SimpleTestCase):
    def test_home_url_resolves(self):
        url = reverse('home')
        self.assertEquals(resolve(url).func, views.home)

    def test_student_url_resolves(self):
        url = reverse('student')
        self.assertEquals(resolve(url).func, views.student)

    def test_internship_url_resolves(self):
        url = reverse('internship')
        self.assertEquals(resolve(url).func, views.internship)

    def test_admin_url_resolves(self):
        url = reverse('admin')
        self.assertEquals(resolve(url).func, views.admin)

    def test_contacts_url_resolves(self):
        url = reverse('contacts')
        self.assertEquals(resolve(url).func, views.contacts)

    def test_form_success_url_resolves(self):
        url = reverse('form-success')
        self.assertEquals(resolve(url).func, views.formSuccess)

    def test_form_failure_url_resolves(self):
        url = reverse('form-failure')
        self.assertEquals(resolve(url).func, views.formFailure)
