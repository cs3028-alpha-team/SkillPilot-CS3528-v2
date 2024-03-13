import pandas as pd
from django.conf import settings
from .candidate_analysis import candidate_histogram_code, course_count, job_min_score_count, plot_jobs_remaining_vs_iterations
from django.shortcuts import render
import os
from django.contrib.auth.decorators import login_required
from .decorators import *
from core import gale_shapley
from django.http import JsonResponse

@login_required
@allowed_users(allowed_roles=['Admin'])
def dashboard(request):
    return render(request, 'dashboard.html')

@login_required
@allowed_users(allowed_roles=['Admin'])
def candidate_histogram(request):
    print("Generating candidate histogram...")
    file_path = 'data/processed_candidates.csv'
    candidates = pd.read_csv(file_path)
    chart = candidate_histogram_code(candidates)
    temp_file = os.path.join('data/candidate_histogram_chart.png') 
    chart.figure.savefig(temp_file)
    print("Candidate histogram saved at:", temp_file)
    return JsonResponse({'chart_path': temp_file})

@login_required
@allowed_users(allowed_roles=['Admin'])
def course_count_call(request):
    print("Generating course count chart...")
    file_path = 'data/processed_candidates.csv'
    candidates = pd.read_csv(file_path)
    chart = course_count(candidates)
    temp_file = os.path.join('data/course_count_chart.png') 
    chart.figure.savefig(temp_file)
    print("Course count chart saved at:", temp_file)
    return JsonResponse({'chart_path': temp_file})

@login_required
@allowed_users(allowed_roles=['Admin'])
def job_min_score_count_call(request):
    print("Generating job min score count chart...")
    file_path = 'data/processed_jobs.csv'
    jobs = pd.read_csv(file_path)
    chart = job_min_score_count(jobs)
    temp_file = os.path.join('data/job_min_score_count_chart.png')
    chart.figure.savefig(temp_file)
    print("Job min score count chart saved at:", temp_file)
    return JsonResponse({'chart_path': temp_file})


#def jobs_remaining_vs_iterations_call(request):
    candidates = pd.read_csv('data/processed_candidates.csv')
    jobs = pd.read_csv('data/processed_jobs.csv')
    
    
    performance_data = [gale_shapley(candidates.head(i), jobs.head(j), i, j) for j in range(10, 210, 10) for i in range(5, 55, 5)]

    print("completion test")
    for data in performance_data:
        print(data)

    plot_jobs_remaining_vs_iterations(performance_data)
    print("after test")
    
    return HttpResponse("Plot generated successfully.")
