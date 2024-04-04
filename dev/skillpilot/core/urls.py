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


    
    # paths related to student authentication and authorization
    path('student-signup', views.student_signup, name='studentSignup'),

    # paths available to the admin to query the database from the admin dashboard
    path('query-students', views.query_students, name='queryStudents'),
    path('query-recruiters', views.query_recruiters, name='queryRecruiters'),
    path('query-internships', views.query_internships, name='queryInternships'),

    # display the details page for students, recruiters, and internship listings
    path('student-details/<str:studentID>/', views.student_details, name='studentDetails'),
    path('recruiter-details/<str:recruiterID>/', views.recruiter_details, name='recruiterDetails'),
    path('internship-details/<str:internshipID>/', views.internship_details, name='internshipDetails'),

]