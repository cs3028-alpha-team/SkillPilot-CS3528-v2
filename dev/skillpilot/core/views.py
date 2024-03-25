from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, Http404, JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.urls import reverse
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from django.views import View

from . models import *
from . forms import *
from . decorators import *
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, get_object_or_404
from  .gale_shapley import *
from .data_pipeline import *
import subprocess
import csv
import os
import pandas as pd



# view for the route '/home' 
def home(request):
    return render(request, 'home.html')

# render view upon form submission to notify user of success
@login_required
def formSuccess(request):
    return render(request, 'form-success.html')

@login_required
def formFailure(request):
    return render(request, 'form-failure.html')

# render view for admin page
@login_required
@allowed_users(allowed_roles=['Admin'])
def admin(request):
    
    csv_data = []
    with open('data/offers.csv', 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            csv_data.append(row)
    print(csv_data)
            
    current_internships = Internship.objects.all()  # Fetch all internships from the database
    return render(request, 'admin.html', {'current_internships': current_internships, 'csv_data': csv_data})

# Lives in the dashboard app
@login_required
@allowed_users(allowed_roles=['Admin'])
def dashboard(request):
    return render(request, 'dashboard/dashboard.html')

# render view with admin contact details
def contacts(request):
    return render(request, 'contacts.html')

# render view for login page
def Login(request):
    if request.user.is_authenticated:
        return redirect('student')
    else:
        return render(request, 'Login-Page.html')

# render view for registration page
@unauthenticated_user  
def registration_user(request):
    return render(request, 'student-registration.html')

# render view for registration page
@unauthenticated_user  
def registration_company2(request):
    return render(request, 'company-registration.html')

# render view for Login page  
def employer_Login(request):
    if request.user.is_authenticated:
        return redirect('internship')
    else:
        return render(request, 'Login-company.html')

# render view for Login  
@unauthenticated_user  
def login_admin(request):
    return render(request, 'Login-admin.html')


# view for the route '/student'
@login_required
#@allowed_users(allowed_roles=['Admin']) #change back to companies 
def student(request):
    if request.method == 'POST':
        form = StudentForm(request.POST)

        if form.is_valid():
            email = form.cleaned_data['email']  # Retrieve email address from the form data
            
            # Check if a student with the same email already exists
            existing_student = Student.objects.filter(email=email).first()
            if existing_student:
                # If student with same email exists, update its fields with the new data
                form_data = form.cleaned_data
                existing_student.fullName = form_data['fullName']
                existing_student.currProgramme = form_data['currProgramme']
                existing_student.prevProgramme = form_data['prevProgramme']
                existing_student.studyMode = form_data['studyMode']
                existing_student.studyPattern = form_data['studyPattern']
                existing_student.GPA = form_data['GPA']
                existing_student.desiredContractLength = form_data['desiredContractLength']
                existing_student.willingRelocate = form_data['willingRelocate']
                existing_student.aspirations = form_data['aspirations']

                existing_student.save()  # Save the updated instance
                return redirect('form-success')
            else:
                # If student with same email does not exist, proceed with form submission
                form.save() 
                return redirect('form-success')
        else:
            print(form.errors)
            return redirect('form-failure')
    else:
        form = StudentForm()
        context = {'form': form}
        return render(request, 'student.html', context)

# view for the route '/internship'
@login_required
def internship(request):

    form = InternshipForm()
    context = { 'form' : form }

    # POST request sent on '/internship', trigger registration procedure
    if request.method == 'POST':
        
        # process data and register internship to database
        form = InternshipForm(request.POST)

        if form.is_valid():

            form.save() 

            return redirect('form-success')

        else:
            print("=================== errors ========================")
            print(form.errors)
            print(request.POST)
            return redirect('form-failure')

    # serve the registration form for new internships
    else:
        return render(request, 'internship.html', context)
    
# view to render the details of a specific internship opportunity
def internshipDetails(request, internshipID):
    # Fetch the internship object using the provided ID
    internship = get_object_or_404(Internship, pk=internshipID)

    if request.method == 'POST':
        # Process form submission if it's a POST request
        form = InternshipForm(request.POST, instance=internship)
        if form.is_valid():
            form.save()
            # Redirect to a success page or render the same page with a success message
    else:
        # Render the form with the internship object
        form = InternshipForm(instance=internship)

    context = {'form': form, 'internship': internship}
    return render(request, 'internship-details.html', context)
    
 # view to handle login
@unauthenticated_user  
def login_user(request):
    if request.method == "POST":
        username = request.POST.get('user_name')
        password = request.POST.get('password')
        next_url = request.GET.get('next')  # get the 'next' parameter from the URL

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if next_url:  #if 'next' parameter exists, redirect to that URL
                return HttpResponseRedirect(next_url)
            else:  # redirect to a default URL
                return render(request, 'student.html')
        else:
            messages.error(request, "Invalid username or password")
            return render(request, 'Login-page.html')

    else:
        # render the login form for GET requests
        return render(request, 'Login-page.html')
    

@unauthenticated_user 
def login_admin(request):
    if request.method == "POST":
        username = request.POST.get('user_name')
        password = request.POST.get('password')
        next_url = request.GET.get('next')  # get the 'next' parameter from the URL

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if next_url:  #if 'next' parameter exists, redirect to that URL
                return HttpResponseRedirect(next_url)
            else:  # redirect to a default URL
                return render(request, 'admin.html')
        else:
            messages.error(request, "Invalid username or password")
            return render(request, 'Login-admin.html')

    else:
        # render the login form for GET requests
        return render(request, 'Login-admin.html')

@unauthenticated_user      
def login_internship(request):
    if request.method == "POST":
        username = request.POST.get('user_name')
        password = request.POST.get('password')
        next_url = request.GET.get('next')  # get the 'next' parameter from the URL

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if next_url:  #if 'next' parameter exists, redirect to that URL
                return HttpResponseRedirect(next_url)
            else:  # redirect to a default URL
                return render(request, 'internship.html')
        else:
            messages.error(request, "Invalid username or password")
            return render(request, 'Login-company.html')

    else:
        # render the login form for GET requests
        return render(request, 'Login-company.html')

    
 # view to handle logout
def logout_user(request):
    logout(request)
    return redirect('home') 

#handle registration of companies
@unauthenticated_user   
def registering_company(request):
    if request.method == "POST":
        form = CreateCompanyForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            group = Group.objects.get(name = 'Companies') #assigning user to group when the account is created 
            user.groups.add(group)

            messages.success(request, 'Account was created for ' + username)
            return redirect('Login-company')  # Redirect to the Login-company page after successful registration
    else:
        form = UserCreationForm()
    
    context = {'form': form}
    return render(request, 'company-registration.html', context)



@unauthenticated_user   
def registering_user(request):
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username') 
            group = Group.objects.get(name = 'Students') #assigning user to group when the account is created
            user.groups.add(group)
            messages.success(request, 'Account was created for ' + username)
            return redirect('Login-page')  # Redirect to the Login page after successful registration
    else:
        form = UserCreationForm()
    
    print(form.errors)
    context = {'form': form}
    return render(request, 'student-registration.html', context)

@login_required
def delete_user(request): 
    if request.method == 'POST':
        user = request.user

        # Delete forms connected to the user
        Student.objects.filter(email=user.email).delete()

        # Delete the user
        user.delete()

        logout(request)
        return redirect('home')
    else:
        # Handle GET request, if needed
        return redirect('home')
    
@login_required
@allowed_users(allowed_roles=['Admin'])
def CurrentInternship(request):
    current_internships = Internship.objects.all()
    return render(request, 'internship.html', {'current_internships': current_internships}) 

@login_required
@allowed_users(allowed_roles=['Admin'])
def cancel_internship(request, internshipID):
    internship = Internship.objects.get(pk=internshipID)
    internship.delete()
    return redirect('admin')  # Redirect back to the admin page after deletion

@login_required
@allowed_users(allowed_roles=['Admin'])
def clean_data(request):

    # Call the data processing function
    jobs, candidates = process_data()

    # Save the processed dataframes to CSV files
    jobs.to_csv('data/processed_jobs.csv', index=False)
    candidates.to_csv('data/processed_candidates.csv', index=False)

    return HttpResponse('Data processed successfully')

@login_required
@allowed_users(allowed_roles=['Admin']) 
def matching_view(request):
    if request.method == 'POST':
        # Call the compute_compatibility_matrix function
        compatibility_matrix = compute_compatibility_matrix(students, internships)
        
        # Save compatibility_matrix to a CSV file
        csv_file_path = 'data/compatibility_matrix.csv'
        with open(csv_file_path, 'w', newline='') as csvfile:  # Open in write mode ('w')
            writer = csv.writer(csvfile)
            
            # Write header row
            writer.writerow(['Candidate IDs'] + [str(job_id) for job_id in compatibility_matrix.columns])
            
            # Write compatibility data
            for index, row in compatibility_matrix.iterrows():
                writer.writerow([index] + row.tolist())
                
        return HttpResponse('Matching process completed. Compatibility matrix saved to CSV file.')
    else:
        return HttpResponse('Error: POST request expected.')

@login_required
@allowed_users(allowed_roles=['Admin']) 
def run_matching_algorithm(request):
    candidates = pd.read_csv('data/processed_candidates.csv')
    jobs = pd.read_csv('data/processed_jobs.csv')
    number_of_candidates = len(candidates)
    number_of_jobs = len(jobs)
    compatibility_matrix = compute_compatibility_matrix2(candidates, jobs) 

    print(compatibility_matrix)
    print(f"Number of candidates: {number_of_candidates}")
    print(f"Number of jobs: {number_of_jobs}")

    offers = run_gale_shapley(candidates, jobs, number_of_candidates, number_of_jobs) # error here 
    print("offersssssssw")
    print(offers)
    print(" ================ offers ========================")
    formatted_pairings = format_pairings(offers, candidates, jobs)
   
    # save_results_to_csv function is in the matching.py file
    output_file = 'data/offers.csv' 
    save_results_to_csv(formatted_pairings, output_file)
    
#    return JsonResponse({'status': 'success'})
    
    # Construct the HTML string with the link
    html = "Matching algorithm executed successfully. Results saved to CSV file. <a href='/admin_page'>Admin</a>"
    return HttpResponse(html)

@login_required
@allowed_users(allowed_roles=['Admin'])
def execute_matching_process(request):
    # Call clean_data function
    clean_data_response = clean_data(request)
    if clean_data_response.status_code == 200:# checks if successful
        # Call matching_view function
        matching_view_response = matching_view(request)
        if matching_view_response.status_code == 200:
            # Call run_matching_algorithm function
            return run_matching_algorithm(request)
        else:
            return matching_view_response
    else:
        return clean_data_response

#only shows student details
def match_detail(request, student, internship):
    student_num = get_object_or_404(Student, pk=student)
    internship_num = get_object_or_404(Internship, pk=internship)

    return render(request, 'match_detail.html', {'student': student_num, 'internship': internship_num})    

def approve_match(request, id):
    approved_matches = pd.read_csv('data/approved_offers.csv')
    matches = pd.read_csv('data/offers.csv')
    approved_match = matches[matches['Candidate_id'] == int(id)]
    approved_matches = pd.concat([approved_matches, approved_match], ignore_index=True)
    matches.drop(approved_match.index, inplace=True)

    matches.to_csv('data/offers.csv', index=False, header=["Student_num","Candidate_id","Student","Student_course","Internship_id","Internship","Internship-Position"])
    approved_matches.to_csv('data/approved_offers.csv', index=False, header=["Student_num","Candidate_id","Student","Student_course","Internship_id","Internship","Internship-Position"])
    
    html = "Match approved successfully. Results saved to CSV file. <a href='/admin_page'>Admin</a>"
    return HttpResponse(html)

def disapprove_match(request, id):
    matches = pd.read_csv('data/offers.csv')
    match = matches[matches['Candidate_id'] == int(id)]
    matches.drop(match.index, inplace=True)
    matches.to_csv('data/offers.csv', index=False, header=["Student_num","Candidate_id","Student","Student_course","Internship_id","Internship","Internship-Position"])
    
    html = "Match dispproved successfully. Results saved to CSV file. <a href='/admin_page'>Admin</a>"
    return HttpResponse(html)
    
#function to send an email
def send_email(request): 
    internships = Internship.objects.all() #get data from database
    students = Student.objects.all()
        
    subject = "Successful application match"

    for student in students:
        name = student.fullName
        context = {'name': name}
        
        html_message = render_to_string('email.html', context)
        text_message = strip_tags(html_message)
        
        mail = EmailMultiAlternatives(
                    subject = subject, #subject
                    body = text_message, #plain text version of message
                    from_email = settings.EMAIL_HOST_USER, #from email display name
                    to = [student.email] #recipient's email      
                )
        
        mail.attach_alternative(html_message, 'text/html')
        mail.send()
        
    return HttpResponse('Email sent')

def search_student(request):
    context_object_name = 'all_search_results'
    template = 'search_student.html'
    
    student_name_input = request.GET.get('studentNameInput')
    student_email_input = request.GET.get('studentEmailInput')
    student_id_input = request.GET.get('studentIDInput')
    object_list = Student.objects.all()
    
    if student_name_input:
        object_list = object_list.filter(fullName__icontains=student_name_input)
    if student_email_input:
        object_list = object_list.filter(email__icontains=student_email_input)
    if student_id_input:
        object_list = object_list.filter(studentID__icontains=student_id_input)    
    
    return render(request, template, {context_object_name: object_list})

def student_detail(request, student):
    student_id = get_object_or_404(Student, pk=student)
    return render(request, 'student_detail.html', {'student': student_id})   