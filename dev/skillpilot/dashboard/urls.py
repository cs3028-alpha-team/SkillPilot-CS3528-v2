from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('candidate-histogram/', views.candidate_histogram, name='candidate_histogram'),
    path('course_count/', views.course_count_call, name='course_count_call'),
    path('job_min_score_count_call/', views.job_min_score_count_call, name='job_min_score_count_call'),
   # path('generate_plot/', views.jobs_remaining_vs_iterations_call, name='generate_plot'),

    
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)