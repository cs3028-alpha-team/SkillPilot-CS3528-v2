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

]