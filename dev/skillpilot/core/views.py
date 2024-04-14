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
from django.contrib.auth.models import User
from .decorators import *
from django.shortcuts import get_object_or_404


def CurrentInternship(request):
    current_internships = Internship.objects.all() #takes all internship database information
    return render(request, 'internship.html', {'current_internships': current_internships}) 

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



# ========================================= General Purpose views ============================================ #

def home(request):
    return render(request, 'home.html')

def contacts(request):
    return render(request, 'contacts.html')



# ========================================= Student, Recruiter, and Admin Dashboard pages ============================================ #

# view for the route '/student'
@login_required
@allowed_users(allowed_roles=['Students']) # access to student accounts only
def student_dashboard(request):
    if request.method == 'POST':
        form = StudentForm(request.POST)

        if form.is_valid():
            email = form.cleaned_data['email']  # Retrieving email address from the form data
            
            # Check if a student with the same email already exists
            existing_student = Student.objects.filter(email=email).first()
            if existing_student:
                # If student with same email exists the information for that email is updated 
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

                existing_student.save()  # Saving the updated instance
                messages.success(request, 'Form successful!')
                return redirect('student')  
            else: 
                # If student with same email does not exist from is a success
                form.save() 
                messages.success(request, 'Form successful!')
                return redirect('student')  
        else:
            messages.error(request, 'Form unsuccessful try again') 
            return redirect('student')
    else:
        form = StudentForm()
        context = {'form': form}
        return render(request, 'student_dashboard.html', context)


def admin(request):
    return render(request, 'admin.html')


# view for the route '/internship'
# view for the route '/internship'
@login_required
@allowed_users(allowed_roles=['Companies']) 
def internship(request):
    form = InternshipForm()

    # Get the logged-in recruiter
    #recruiter = Recruiter.objects.get(fullName=request.user)
    context = { 'form' : form }
    # Pass the recruiter's company ID to the template context
    #context = {'form': form, 'company_id': recruiter.companyID.companyID}

    if request.method == 'POST':
        form = InternshipForm(request.POST)
        if form.is_valid():
            form.save() 
            messages.success(request, 'Form successful!')
            return redirect('internship')
        else:
            messages.error(request, 'Form unsuccessful try again')
            return redirect('internship')
    else:
        return render(request, 'internship.html', context) 


# ========================================= Admin Dashboard - Companies Management Tool functionalities ============================================ #

# handle the companies management tool functionality
@login_required
@allowed_users(allowed_roles=['Admin']) 
def companies_management_tool(request):
    
    context = {}

    # query all companies from the database
    companies = Company.objects.all().order_by('companyName')

    # link a recruiter (if any) to each company in the database
    for company in companies:

        # query the database for a recruiter whose companyID field matches the current company's companyID
        recruiter = None
        try: recruiter = Recruiter.objects.get(companyID=company.companyID)
        except: pass

        # attach the recruiter object found to the current company
        company.recruiter = recruiter

    context['companies'] = companies

    # the request comes from the dropdown menu to filter company listings
    if request.method == 'POST':

        filter_condition = request.POST.get('companyFilterDrowpdown')

        # if filter_condition is 'all', we simply pass the above context dictionary into the template as it is

        # construct lists of companies linked and not linked to a recruiter account 
        linked, unlinked = [], []
        for company in companies:

            try:
                recruiter = Recruiter.objects.get(companyID=company.companyID)
                linked.append(company)
            except:
                unlinked.append(company)

        # check for the filter condition, and return the appropriate list to the user
        context['companies'] = linked if filter_condition == 'claimed' else unlinked

    return render(request, 'companies_management_tool.html', context=context)

# handle the companies management tool delete functionality
@login_required
@allowed_users(allowed_roles=['Admin']) 
def delete_company(request, companyID):

    if request.method == 'POST':

        # Retrieve the recruiters email before deleting the recruiter
        try:
            recruiter = Recruiter.objects.get(companyID=companyID)
            recruiter_email = recruiter.email
        except: pass

        # Delete the recruiter account associated with the current company
        try:
            recruiter.delete()
        except: pass

        # Delete any internship listings associated with the company
        try:
            Internship.objects.filter(companyID=companyID).delete()
        except: pass
        
        # Delete the company listing
        try:
            Company.objects.get(companyID=companyID).delete()
        except: pass
          

        # Delete the user associated with the company by email
        if recruiter_email:
            try:
                user = User.objects.get(email=recruiter_email)
                user.delete()
            except: pass
        messages.success(request, 'Company deleted successfully. Please contact the recruiter to inform them of the action')
        return redirect('manage-companies')

    return render(request, 'companies_management_tool.html')

# ========================================= Authentication (Login & Signup) and Authorization logic ============================================ #

# handle the signup routine for a new student
def student_signup(request):
    if request.user.is_authenticated:
        return redirect('student')
    if request.method == 'POST':
        payload = {
            'username': request.POST.get('studentUsername'),
            'email': request.POST.get('studentEmail'),
            'password1': request.POST.get('studentPassword1'),
            'password2': request.POST.get('studentPassword1')
        }
        
        new_student = StudentSignupForm(payload)
        
        if new_student.is_valid():
            new_student = User.objects.create_user(username=payload['username'], email=payload['email'], password=payload['password1'])
            group = Group.objects.get(name='Students')
            new_student.groups.add(group)

            messages.success(request, 'Signup successful!')
            return redirect('student-login')
        else:
            messages.info(request, 'Looks like you already have an account, please login!')
            return redirect('student-login')

    return render(request, 'auth/student_signup.html')


# handle the login routine for a returning student
def student_login(request):
    if request.user.is_authenticated:
        return redirect('student')
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
    if request.user.is_authenticated:
        return redirect('internship')
    
    if request.method == 'POST':
        # Extract recruiter details from the form
        recruiter_username = request.POST.get('recruiterUsername')
        recruiter_email = request.POST.get('recruiterEmail')
        recruiter_token = request.POST.get('recruiterToken')
        recruiter_id = request.POST.get('recruiterID')
        recruiter_job_title = request.POST.get('recruiterJobTitle')
        password1 = request.POST.get('recruiterPassword1')
        password2 = request.POST.get('recruiterPassword2')

        # Check if the recruiter token matches a companyID in the database
        try:
            company = Company.objects.get(companyID=recruiter_token)
        except Company.DoesNotExist:
            messages.error(request, 'Invalid recruiter token. Please enter a valid recruiter token.')
            return redirect('recruiter-signup')

        # Check if passwords match
        if password1 != password2:
            messages.error(request, 'Passwords do not match.')
            return redirect('recruiter-signup')

        # Check if the username already exists
        if User.objects.filter(username=recruiter_username).exists():
            messages.error(request, 'Username already exists. Please choose a different username.')
            return redirect('recruiter-signup')
        
        # Create the recruiter account if all validations pass
        user = User.objects.create_user(username=recruiter_username, email=recruiter_email, password=password1)
        group = Group.objects.get(name = 'Companies')
        user.groups.add(group)
        recruiter = Recruiter.objects.create(
            fullName=user.username, 
            email=user.email,  
            recruiterID=recruiter_id,
            companyID=company,
            jobTitle=recruiter_job_title
        )

        messages.success(request, 'Recruiter account created successfully. Please login.')
        return redirect('recruiter-login')

    return render(request, 'auth/recruiter_signup.html')

# handle the login routine for returning recruiters
def recruiter_login(request):
    if request.user.is_authenticated:
        return redirect('internship')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        # If user is authenticated, log them in and redirect to the recruiter form page
        if user is not None:
            login(request, user)
            return redirect('internship')  # Adjust this to the correct URL name for the recruiter form page
        else:
            # If authentication fails, display an error message
            messages.error(request, 'Invalid username or password.')
            return redirect('recruiter-login') 

    return render(request, 'auth/recruiter_login.html')

# handle the login of admin using MFA
def admin_login(request):
    return render(request, 'auth/admin_login.html')

# handle the logout routine for all app users
def user_logout(request):
    # logout user in current session
    logout(request)

    messages.success(request, 'logout successfull')  
    return redirect('home')

# register a new company to the database using the payload from the form submitted from the companies management tool
@login_required
@allowed_users(allowed_roles=['Admin']) 
def register_company(request):

    if request.method == 'POST':

        # extract the new company details from the request payload
        payload = {
            'companyID' : request.POST.get('recruiterToken'),
            'companyName' : request.POST.get('companyName'),
            'industrySector' : request.POST.get('companyField'),
            'websiteURL' : request.POST.get('companyWebsite')
        }

        # instantiate a new company using the Company model and request payload
        new_company = CompanyRegistrationForm(payload)

        if new_company.is_valid():
            new_company.save()
            messages.success(request, 'Company successfully registered!')
    
        else:
            messages.info(request, 'Error occured while registering company, possibly caused by duplicate company!')
        
        return redirect('manage-companies')

    return render(request, 'companies_management_tool.html')

# view to handle logout
@login_required
def logout_user(request):
    logout(request)
    return render(request, 'home.html')

# ========================================= Student, Recruiters, and Internships detail pages ============================================ #

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
    
# ========================================= Admin Dashboard Query Database functionality ============================================ #

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


# ========================================= Recruiter and internship delete function ============================================ #
@login_required
@allowed_users(allowed_roles=['Students']) 
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
        
        return redirect('home')
    
@login_required
@allowed_users(allowed_roles=['Companies']) 
def delete_recruiter(request):
    if request.method == 'POST':
        recruiter = request.user  # Get the logged-in recruiter
        recruiter_email = recruiter.email
        print("adsaasasad", recruiter)
        print("adsaasasad", recruiter_email)
        # Delete the recruiter account associated with the current company
        #try:
            #recruiter.delete()
        #except: 
         #   print("Error deleting recruiter:", sys.exc_info()[0])

        # Delete any internship listings associated with the company
        try:
            Internship.objects.filter(recruiterID=recruiter.recruiterID).delete()
            print("Internships deleted successfully")
        except:
            print("Error deleting internships:", sys.exc_info()[0])

        # Delete the user associated with the company by email
        if recruiter_email:
            try:
                user = User.objects.get(email=recruiter_email)
                user.delete()
            except:
                print("Error deleting user:", sys.exc_info()[0])

        messages.success(request, 'Company deleted successfully. Please contact the recruiter to inform them of the action')
        logout(request)
        return redirect('home')
    else:
        return redirect('home')
    