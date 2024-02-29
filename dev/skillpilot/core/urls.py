from django.urls import path
from . import views 

urlpatterns = [
    path('', views.home, name='home'),
    path('student', views.student, name='student'),
    path('internship', views.internship, name='internship'),
    path('form-success', views.formSuccess, name='form-success'),
]