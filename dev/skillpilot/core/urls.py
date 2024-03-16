from django.urls import path
from . import views 
from .views import clean_data

urlpatterns = [

    path('', views.home, name='home'),

    path('home', views.home, name='home'),

    path('student', views.student, name='student'),

    path('internship', views.internship, name='internship'),

    # this view will take in an internship ID and then dynamically load the contents from the database
    path('internship-details/<str:internshipID>/', views.internshipDetails, name='internship-details'),

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

    path('registering_user', views.registering_user, name='registering_user'),

    path('delete-user/', views.delete_user, name='delete_user'),

    path('current-internships', views.CurrentInternship, name='current-internships'),

    path('clean-data/', views.clean_data, name='clean_data'),

    path('matching', views.matching_view, name='matching'),

    path('run_matching_algorithm', views.run_matching_algorithm, name='run_matching_algorithm'),

    path('cancel_internship/<str:internshipID>/', views.cancel_internship, name='cancel_internship'),

    path('execute_matching_process/', views.execute_matching_process, name='execute_matching_process'),
]