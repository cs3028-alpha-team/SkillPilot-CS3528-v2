from django.urls import path
from . import views 

urlpatterns = [
    path('', views.home, name='home'),
    path('student', views.student, name='student'),
    path('internship', views.internship, name='internship'),
    path('admin', views.admin, name='admin'),
    path('contacts', views.contacts, name='contacts'),
    path('form-success', views.formSuccess, name='form-success'),
    path('form-failure', views.formFailure, name='form-failure'),
]