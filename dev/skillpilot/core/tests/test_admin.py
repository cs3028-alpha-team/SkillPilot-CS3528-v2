from django.contrib import admin
from django.test import TestCase
from core.models import Student, Internship, Company, Recruiter, Interview, computedMatch, SuperUser

#test admin page model registrations
class AdminTests(TestCase):
    def test_student_registered(self):
        self.assertIn(Student, admin.site._registry)

    def test_internship_registered(self):
        self.assertIn(Internship, admin.site._registry)

    def test_company_registered(self):
        self.assertIn(Company, admin.site._registry)

    def test_recruiter_registered(self):
        self.assertIn(Recruiter, admin.site._registry)

    def test_interview_registered(self):
        self.assertIn(Interview, admin.site._registry)

    def test_computedmatch_registered(self):
        self.assertIn(computedMatch, admin.site._registry)

    def test_superuser_registered(self):
        self.assertIn(SuperUser, admin.site._registry)
