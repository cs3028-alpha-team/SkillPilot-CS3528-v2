import pandas as pd
from django.conf import settings
from .candidate_analysis import candidate_histogram_code, course_count, job_min_score_count, plot_jobs_remaining_vs_iterations
from django.shortcuts import render
import os
import tempfile


def dashboard(request):
    return render(request, 'dashboard.html')


def candidate_histogram(request):
    # Data is taken form processed_candidates.py in the data folder
    # Set file path to get the information for the histogram
    file_path = 'data/processed_candidates.csv'
    
    #read the file
    candidates = pd.read_csv(file_path)
    
    # call the function in the candidate_analysis.py file using the data from processed_candidates.py
    chart = candidate_histogram_code(candidates)

    # Define the path for saving the chart image
    image_path = os.path.join(settings.MEDIA_ROOT, 'histogram_chart.png')

    # Save the chart image
    chart.figure.savefig(image_path)
    
    if request.method == 'POST':
        active_tab = request.POST.get('active_tab', 'candidate_histogram')
    else:
        # Set the default value if the form is not submitted
        active_tab = 'candidate_histogram'

    # Return the path to the saved image with active_tab set
    return render(request, 'dashboard.html', {'chart_path': image_path, 'active_tab': active_tab})




def course_count_call(request):
    # Data is taken from processed_candidates.py in the data folder
    # Set file path to get the information for the histogram
    file_path = 'data/processed_candidates.csv'
    
    # Read the file
    candidates = pd.read_csv(file_path)
    
    # Define the path for the temporary chart image
    temp_file = os.path.join(settings.BASE_DIR, 'data', 'course_count_chart.png')    
    
    # Check if the chart image already exists and delete it to show newer data
    if os.path.exists(temp_file):
        os.remove(temp_file)
    
    # Call the candidate_count function to generate the histogram chart
    chart = course_count(candidates)
    chart.figure.savefig(temp_file)
    
    # Check if the form is submitted
    if request.method == 'POST':
        active_tab = request.POST.get('active_tab', 'course_count')
    else:
        # Set the default value if the form is not submitted
        active_tab = 'course_count'

    # Return the path to the saved image with active_tab set
    return render(request, 'dashboard.html', {'chart_path': temp_file, 'active_tab': active_tab})


    




def job_min_score_count_call(request):
    file_path = 'data/processed_jobs.csv'
    jobs = pd.read_csv(file_path)
    temp_file = os.path.join(settings.BASE_DIR, 'data', 'job_min_score_count_chart.png')
    
    # Check if the chart image already exists and delete it to show newer data
    if os.path.exists(temp_file):
        os.remove(temp_file)
    
     # Call the candidate_count function to generate the histogram chart
    chart = job_min_score_count(jobs)
    chart.figure.savefig(temp_file)
    
    # Check if the form is submitted
    if request.method == 'POST':
        active_tab = request.POST.get('active_tab', 'job_min_score_count')
    else:
        # Set the default value if the form is not submitted
        active_tab = 'job_min_score_count'

    # Return the path to the saved image with active_tab set
    return render(request, 'dashboard.html', {'chart_path': temp_file, 'active_tab': active_tab})





#def jobs_remaining_vs_iterations_call(request):
    candidates = pd.read_csv('data/processed_candidates.csv')
    jobs = pd.read_csv('data/processed_jobs.csv')
    
    
    performance_data = [run_gale_shapley(candidates.head(i), jobs.head(j), i, j) for j in range(10, 210, 10) for i in range(5, 55, 5)]

    print("completion test")
    for data in performance_data:
        print(data)

    plot_jobs_remaining_vs_iterations(performance_data)
    print("after test")
    
    return HttpResponse("Plot generated successfully.")
