from django.urls import path
from . import views 

urlpatterns = [

    path('', views.home, name='home'),

    path('student', views.student, name='student'),

    path('internship', views.internship, name='internship'),

    # this view will take in an internship ID and then dynamically load the contents from the database
    path('internship-details', views.internshipDetails, name='internship-details'),

    path('admin', views.admin, name='admin'),

    path('contacts', views.contacts, name='contacts'),

    path('form-success', views.formSuccess, name='form-success'),

    path('form-failure', views.formFailure, name='form-failure'),

    path('Login-page', views.Login, name = 'Login-page'),

    path('login_user', views.login_user, name = "login_user"),

    path('Admin-login', views.login_admin, name='Admin-login'),

    path('login_internship', views.login_internship, name = "login_internship"),

    path('Login-company', views.employer_Login, name='Login-company'),

    path('logout', views.logout_user, name='logout'),

    path('student-registration', views.registration_user, name='student-registration'),

    path('Company-registration', views.registration_company2, name='Company-registration'),

    path('registering_company', views.registering_company, name='registering_company'),
    
    path('dashboard/', views.dashboard, name='dashboard'),
]