from django.urls import path
from . import views 
from .views import clean_data

urlpatterns = [

    path('', views.home, name='home'),

    path('home', views.home, name='home'),

    path('internship', views.internship, name='internship'),

    path('admin_page', views.admin, name='admin_page'),

    path('contacts', views.contacts, name='contacts'),

    path('dashboard/', views.dashboard, name='dashboard'),

    path('current-internships', views.CurrentInternship, name='current-internships'),

    path('clean-data/', views.clean_data, name='clean_data'),

    path('matching', views.matching_view, name='matching'),

    path('run_matching_algorithm', views.run_matching_algorithm, name='run_matching_algorithm'),

    path('cancel_internship/<str:internshipID>/', views.cancel_internship, name='cancel_internship'),

    path('execute_matching_process/', views.execute_matching_process, name='execute_matching_process'),
    
    path('approve_match/<str:id>/', views.approve_match, name='approve_match'),
    
    path('disapprove_match/<str:id>/', views.disapprove_match, name='disapprove_match'),
    
    path('send-email', views.send_email, name="send-email"),


    # path to an authenticated student dashboard
    path('student', views.student_dashboard, name='student'),

    # path to companies management tool, accessible via the admin dashboard
    path('manage-companies', views.companies_management_tool, name='manage-companies'),

    # paths related to student authentication and authorization
    path('student-signup', views.student_signup, name='student-signup'),
    path('student-login', views.student_login, name='student-login'),

    # path related to admin authentication and authorization
    path('admin-login', views.admin_login, name='admin-login'),

    # paths related to recruiter authentication and authorization
    path('recruiter-signup', views.recruiter_signup, name='recruiter-signup'),
    path('recruiter-login', views.recruiter_login, name='recruiter-login'),

    # logout route generalized to all users 
    path('logout', views.user_logout, name='logout'),

    # paths available to the admin to query the database from the admin dashboard
    path('query-students', views.query_students, name='query-students'),
    path('query-recruiters', views.query_recruiters, name='query-recruiters'),
    path('query-internships', views.query_internships, name='query-internships'),

    # display the details page for students, recruiters, and internship listings
    path('student-details/<str:studentID>/', views.student_details, name='student-details'),
    path('recruiter-details/<str:recruiterID>/', views.recruiter_details, name='recruiter-details'),
    path('internship-details/<str:internshipID>/', views.internship_details, name='internship-details'),
]