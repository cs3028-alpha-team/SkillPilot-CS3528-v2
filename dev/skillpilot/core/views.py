from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, Http404, JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group, auth
from django.urls import reverse
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from django.views import View

from . models import *
from . forms import *
from  .gale_shapley import *
from .data_pipeline import *
import subprocess
import csv
import os
import pandas as pd
from django.db.models import Q


def home(request):
    return render(request, 'home.html')

def admin(request):
    
    csv_data = []
    with open('data/offers.csv', 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            csv_data.append(row)
            
    current_internships = Internship.objects.all()  # Fetch all internships from the database
    return render(request, 'admin.html', {'current_internships': current_internships, 'csv_data': csv_data})

def dashboard(request):
    return render(request, 'dashboard/dashboard.html')

# render view with admin contact details
def contacts(request):
    return render(request, 'contacts.html')

# view for the route '/internship'
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
            return redirect('form-failure')

    # serve the registration form for new internships
    else:
        return render(request, 'internship.html', context)
    

def CurrentInternship(request):
    current_internships = Internship.objects.all() #takes all internship database information
    return render(request, 'internship.html', {'current_internships': current_internships}) 


def cancel_internship(request, internshipID):
    internship = Internship.objects.get(pk=internshipID)
    internship.delete()
    return redirect('admin')  # Redirect back to the admin page 

def clean_data(request):

    # Calling the data processing function
    jobs, candidates = process_data()

    # Save the processed dataframes to CSV files
    jobs.to_csv('data/processed_jobs.csv', index=False)
    candidates.to_csv('data/processed_candidates.csv', index=False)

    return HttpResponse('Data processed successfully')

def matching_view(request):
    if request.method == 'POST':
        # Calling the compute_compatibility_matrix function
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

def run_matching_algorithm(request):
    candidates = pd.read_csv('data/processed_candidates.csv') #assigning csv
    jobs = pd.read_csv('data/processed_jobs.csv')
    number_of_candidates = len(candidates) #checking length of candidates
    number_of_jobs = len(jobs) #checking length of jobs
    compatibility_matrix = compute_compatibility_matrix2(candidates, jobs) 
   
    # save_results_to_csv function is in the matching.py file
    output_file = 'data/offers.csv' 
    save_results_to_csv(formatted_pairings, output_file)
    
    #return JsonResponse({'status': 'success'})
    
    # Construct the HTML string with the link
    html = "Matching algorithm executed successfully. Results saved to CSV file. <a href='/admin_page'>Admin</a>"
    return HttpResponse(html)

def execute_matching_process(request):
    # Calling clean_data function
    clean_data_response = clean_data(request)
    if clean_data_response.status_code == 200:# checks if successful
        # Calling matching_view function
        matching_view_response = matching_view(request)
        if matching_view_response.status_code == 200:
            # Calling run_matching_algorithm function
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






# view for the route '/student'
@login_required(login_url='student-login')
def student_dashboard(request):

    return render(request, 'student_dashboard.html')





# handle the signup routine for a new student
def student_signup(request):

    if request.method == 'POST':

        # extract the form's signup credentials
        payload = {
            'username' : request.POST.get('studentUsername'),
            'email' : request.POST.get('studentEmail'),
            'password1' : request.POST.get('studentPassword1'),
            'password2' : request.POST.get('studentPassword1')
        }

        # instantiate the StudentSignupForm using the request payload
        new_student = StudentSignupForm(payload)

        # save the student credentials and redirect them to the student dashboard page
        if new_student.is_valid():
            new_student.save()
            
            # success flash message for student signup
            messages.success(request, 'Signup successfull!')
            return redirect('student')
    
        else:
            messages.info(request, 'Looks like you already have an account, please login!')
            return redirect('student-login')

    return render(request, 'auth/student_signup.html')

# handle the login routine for a returning student
def student_login(request):
    form = UserLoginForm()
    if request.method == 'POST':
        form = UserLoginForm(request, data=request.POST)

        if form.is_valid():
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)

            if user is not None:
                auth.login(request, user)
                messages.success(request, 'login successfull')  
                return redirect('student')

        else:       
            messages.error(request, 'Login failed! please try again or signup for an account')
            return redirect('student-signup')

    return render(request, 'auth/student_login.html')


# handle the signup routine for new recruiters
def recruiter_signup(request):
    return render(request, 'auth/recruiter_signup.html')


# handle the login routine for returning recruiters
def recruiter_login(request):
    return render(request, 'auth/recruiter_login.html')

# handle the logout routine for all app users
def user_logout(request):
    # logout user in current session
    logout(request)

    messages.success(request, 'logout successfull')  
    return redirect('home')



# render a given student profile's details page
def student_details(request, studentID):
    try:
        student = Student.objects.get(studentID = studentID)
        return render(request, 'student_details.html', context={ 'student' : student })
    except:
        messages.error(request, 'Looks like no student with that ID exists!')
        return redirect('query-students')

# render a given recruiter profile's details page
def recruiter_details(request, recruiterID):
    try:
        recruiter = Recruiter.objects.get(recruiterID = recruiterID)
        return render(request, 'recruiter_details.html', context={ 'recruiter' : recruiter })
    except:
        messages.error(request, 'Looks like no recruiter with that ID exists!')
        return redirect('query-recruiters')

# render a given live internship's details page
def internship_details(request, internshipID):
    try:    
        internship = Internship.objects.get(internshipID = internshipID)
        return render(request, 'internship_details.html', context={ 'internship' : internship })
    except:
        messages.error(request, 'Looks like no internship with that ID exists!')
        return redirect('query-internships')




# handle the routine triggered from the admin dashboard to query all student profiles
def query_students(request):

    # query the students table and create a dropdown menu options using only the programmes in the current database students
    curr_programme_options = { student.currProgramme for student in Student.objects.all() }
    prev_programme_options = { student.prevProgramme for student in Student.objects.all() }

    context = {'currProgrammeOptions' : curr_programme_options, 'prevProgrammeOptions' : prev_programme_options }

    if request.method == 'POST':

        # extract the form payload
        student_name = request.POST.get('studentFullname')
        prev_programme = request.POST.get('studentPrevProgramme')
        curr_programme = request.POST.get('studentCurrProgramme')
        filterby = '-GPA' if request.POST.get('resultsFilterby') == 'gpa-desc' else 'GPA'

        # check whether all fields in the POST request are empty
        empty_form = True if "".join([student_name, prev_programme, curr_programme]) == "" else False

        # if form is empty, return the entire student table othewise query db using form parameters
        context['students'] = Student.objects.all().order_by(filterby) if empty_form else Student.objects.filter( Q(fullName=student_name) | Q(currProgramme=curr_programme) | Q(prevProgramme=prev_programme) ).order_by(filterby)

    return render(request, 'admin_search_feature/students_db_query.html', context=context)

# handle the routine triggered from the admin dashboard to query all recruiter profiles
def query_recruiters(request):

    # fetch all the company names stored in the recruiters database using the recruiter.companyID attribute
    ids = [ recruiter.companyID for recruiter in Recruiter.objects.all() ]
    all_companies = { Company.objects.get(companyID = id.companyID).companyName for id in ids }

    context = { 'allCompanies' : sorted(all_companies) }

    if request.method == 'POST':

        # extract the form payload
        recruiter_fullname = request.POST.get('recruiterFullname')
        recruiter_jobtitle = request.POST.get('recruiterJobTitle')
        # only fetch the company name if company is not the default empty placeholder 
        recruiter_company = Company.objects.get(companyName = request.POST.get('recruiterCompany')).companyID if request.POST.get('recruiterCompany') != "" else ""

        # check whether all fields in the POST request are empty
        empty_form = True if "".join([recruiter_fullname, recruiter_jobtitle, recruiter_company]) == "" else False

        # if form is empty, return the entire recruiter table othewise query db using form parameters
        if empty_form:
            context['recruiters'] = Recruiter.objects.all()
        else:
            context['recruiters'] = Recruiter.objects.filter( Q(fullName=recruiter_fullname) | Q(companyID=recruiter_company) | Q(jobTitle=recruiter_jobtitle) )

    return render(request, 'admin_search_feature/recruiters_db_query.html', context=context)

# handle the routine triggered from the admin dashboard to query live internships
def query_internships(request):

    # fetch all the company names stored in the recruiters database using the recruiter.companyID attribute
    company_ids = [ internship.companyID for internship in Internship.objects.all() ]
    all_companies = { Company.objects.get(companyID = id.companyID).companyName for id in company_ids }

    
    # fetch all recruiters which have posted at least one internship
    recruiter_ids = [ internship.recruiterID for internship in Internship.objects.all() ]
    all_recruiters = { Recruiter.objects.get(recruiterID = id.recruiterID).fullName for id in recruiter_ids }

    # fetch all internship fields in the database
    fields = { internship.field for internship in Internship.objects.all() }

    # fetch all internship titles in the database
    titles = { internship.title for internship in Internship.objects.all() }

    # get the range of positons offered across all internships
    positions = { internship.numberPositions for internship in Internship.objects.all() }

    context = { 
        'allCompanies' : sorted(all_companies),
        'allRecruiters' : sorted(all_recruiters),
        'fields' : sorted(fields),
        'titles' : sorted(titles),
        'positions' : sorted(positions), 
    }

    if request.method == 'POST':

        # extract the form payload
        internship_company = request.POST.get('internshipCompany')
        internship_field = request.POST.get('internshipField')
        internship_title = request.POST.get('internshipTitle')
        sortby = '-minGPA' if request.POST.get('internshipMinGPA') == 'desc' else 'minGPA'

        # check whether all fields in the POST request are empty
        empty_form = True if "".join([internship_company, internship_field, internship_title]) == "" or internship_company == "" else False

        # if form is empty, return the entire recruiter table othewise query db using form parameters
        if empty_form:
            context['internships'] = Internship.objects.all().order_by(sortby)

        else:
            company_id = Company.objects.get(companyName = internship_company).companyID

            context['internships'] = Internship.objects.filter( 
                Q(companyID=company_id) | Q(title=internship_title) | Q(field=internship_field)
            ).order_by(sortby)

        # attach the company name to the internship object, since we only have the internship's company ID for now
        for internship in context['internships']:
            internship.company_name = Company.objects.get(companyID=internship.companyID.companyID).companyName

    return render(request, 'admin_search_feature/internships_db_query.html', context=context)