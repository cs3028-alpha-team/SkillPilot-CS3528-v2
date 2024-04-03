from django.urls import path
from . import views 
from .views import clean_data

urlpatterns = [

    path('', views.home, name='home'),

    path('home', views.home, name='home'),

    path('student', views.student, name='student'),

    path('internship', views.internship, name='internship'),

    path('admin_page', views.admin, name='admin_page'),

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
    
    path('approve_match/<str:id>/', views.approve_match, name='approve_match'),
    
    path('disapprove_match/<str:id>/', views.disapprove_match, name='disapprove_match'),
    
    path('send-email', views.send_email, name="send-email"),
    
    path('search_student', views.search_student, name='search_student'),

    

    # ================== URLs related to admin page search functionality =========================
    path('query-students', views.query_students, name='queryStudents'),
    path('query-recruiters', views.query_recruiters, name='queryRecruiters'),
    path('query-internships', views.query_internships, name='queryInternships'),

    path('student-details/<str:studentID>/', views.student_details, name='studentDetails'),
    path('recruiter-details/<str:recruiterID>/', views.recruiter_details, name='recruiterDetails'),
    path('internship-details/<str:internshipID>/', views.internship_details, name='internshipDetails'),

]