from django.urls import path
from . import views 

urlpatterns = [

    path('', views.home, name='home'),

    path('home', views.home, name='home'),

    path('recruiter', views.recruiter_dashboard, name='recruiter'),

    path('admin_page', views.admin, name='admin_page'),

    path('contacts', views.contacts, name='contacts'),
    
    path('send-email', views.send_email, name="send-email"),

    path('recruiter-update/<str:internship_id>/', views.recruiter_update, name='recruiter-update'),

    path('delete-internship/<str:internship_id>/', views.delete_internship, name='delete-internship'),
   

    # paths to handle admin approval/rejection of matchmaking algorithm output 
    path('approve-match/<str:matchID>/', views.approve_match, name='approve-match'),
    path('reject-match/<str:matchID>/', views.reject_match, name='reject-match'),

    # path to render the algorithm dashboard, where the admin can run the algorithm and manage assignments
    path('algorithm-dashboard', views.algorithm_dashboard, name='algorithm-dashboard'),

    # path to render the analytics dashboard, accessible from the admin page
    path('analytics-dashboard', views.analytics_dashboard, name='analytics-dashboard'),

    # path to an authenticated student dashboard
    path('student', views.student_dashboard, name='student'),

    # path to companies management tool, accessible via the admin dashboard
    path('manage-companies', views.companies_management_tool, name='manage-companies'),

    # path to register a new company using the payload from the form submitted via the companies management tool
    path('register-company', views.register_company, name='register-company'),

    # path to delete a company listing, the recruiter profile associated with it, and all internship listings associated with it
    path('delete-company/<str:companyID>', views.delete_company, name='delete-company'),

    # path to delete a student profile associated, and student application connected to it
    path('delete-user', views.delete_user, name='delete-user'),
    
    # path to delete a recruiter profile associated, and student application connected to it
    path('delete-recruiter', views.delete_recruiter, name='delete-recruiter'),


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

    
    # updates the outcome of an interview to accepted/rejected
    path('update-interview/<interview_id>/', views.update_interview, name='update-interview'),
]