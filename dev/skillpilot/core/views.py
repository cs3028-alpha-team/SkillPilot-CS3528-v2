from django.shortcuts import render, redirect, get_object_or_404
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
from . gale_shapley import *
from . data_pipeline import *
import subprocess
import csv
import os
import pandas as pd
import random
import numpy as np
from django.db.models import Q
from datetime import date
import random

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






# ====================== #
#  General Purpose views #
# ====================== #

def home(request):
    return render(request, 'home.html')

def contacts(request):
    return render(request, 'contacts.html')



# ============================================== #
#  Student, Recruiter, and Admin Dashboard pages #
# ============================================== #

# view for the route '/student'
@login_required(login_url='student-login')
def student_dashboard(request):
    
    #basic interview system 
    
    interviews = Interview.objects.all()
    students = Student.objects.all()
    recruiters = Recruiter.objects.all()
    
    try:
        
        #get student id from student email   
        user = request.user
        student_email = user.email
        student_username = user.username
        
        #get details of match
        student = get_object_or_404(Student, email=student_email)
        interview = get_object_or_404(Interview, studentID=student.studentID)        
        recruiter = get_object_or_404(Recruiter, pk=interview.recruiterID.pk)

        # Generate random date and time
        start_dt = date.today().replace(day=1, month=1).toordinal()
        end_dt = date.today().toordinal()
        random_date = date.fromordinal(random.randint(start_dt, end_dt))

        return render(request, 'student_dashboard.html', {'interview': interview, 'username': student_username, 'recruiter': recruiter, 'date': random_date})
    
    # if no interview exists render page with no interview section
    except Student.DoesNotExist:
        print("Student does not exist")
        return render(request, 'student_dashboard.html')
    
    except Interview.DoesNotExist:
        print("Interview does not exist")
        return render(request, 'student_dashboard.html')

    except Recruiter.DoesNotExist:
        print("Recruiter does not exist")
        return render(request, 'student_dashboard.html')

    except Exception as e:
        print("An error occurred:", e)
        return render(request, 'student_dashboard.html')

# accept/reject an interview
# currently only changes outcome in the database
def update_interview(request, interview_id, new_outcome):
    interview = Interview.objects.get(interviewID=interview_id)
    
    interview.outcome = new_outcome
    interview.save()
    
    return redirect('student')

def admin(request):
    return render(request, 'admin.html')


# ============================================================ #
#  Admin Dashboard - Companies Management Tool functionalities #
# ============================================================ #

# handle the companies management tool functionality
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

# handle the procedure to delete a company from the database
def delete_company(request, companyID):

    if request.method == 'POST':

        # delete the recruiter account associated with the current company
        try: Recruiter.objects.get(companyID=companyID).delete()
        except: pass

        # delete any internship listing associated with the company
        try:Internship.objects.filter(companyID=companyID).delete()
        except: pass

        # delete the company listing
        try: Company.objects.get(companyID=companyID).delete()
        except: pass

        messages.success(request, 'Company deleted successfully. Please contact the recruiter to inform them of the action')
        return redirect('manage-companies')

    return render(request, 'companies_management_tool.html')

# register a new company to the database using the payload from the form submitted from the companies management tool
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



# =========================================== #
# Admin Dashboard - Algorithm Functionalities #
# =========================================== #

# render the algorithm dashboard page, where the admin can compute and manage assignments
def algorithm_dashboard(request):

    if request.method == 'POST':
        # 1. Construct the Students and Internships dataframes 

        """
        As per client requirement, each student should have at most one interview at a time, 
        so the dataframe will be composed of all internships with positions still to be filled in 
        and students with no interviews exclusively
        """

        """
        # uncomment to restore internship number of positions, DO NOT USE IN PRODUCTION
        for internship in Internship.objects.all():
            internship.numberPositions = random.randint(2,5)
            internship.save()
        """

        # construct the Students dataframe 
        students = Student.objects.all()
        pd_students = pd.DataFrame(columns=['studentID', 'prevProgramme', 'GPA', 'studyMode', 'studyPattern'])
        for i in range(len(students)):

            # check that student doesn't have an interview scheduled, i.e. there's not an entry in the interviews table
            try:
                Interview.objects.get(studentID=students[i].studentID)
                pass
            except:
                pd_students.loc[i] = [ students[i].studentID, students[i].prevProgramme, students[i].GPA, students[i].studyMode, students[i].studyPattern ]

        # construct the Internships dataframe
        internships = Internship.objects.all()
        pd_internships = pd.DataFrame(columns=['internshipID', 'companyID', 'field', 'minGPA', 'contractMode', 'contractPattern', 'numberPositions'])
        for i in range(len(internships)):

            # check that internship has still positions to fill, i.e. numberPositions > 0
            if internships[i].numberPositions > 0:
                pd_internships.loc[i] = [ internships[i].internshipID, internships[i].companyID.companyID, internships[i].field, internships[i].minGPA, internships[i].contractMode, internships[i].contractPattern, internships[i].numberPositions ]


        # 2. Prepare the Dataframes for the matchmaking operation, using the DataPipeline class
        pipeline = DataPipeline(pd_students, pd_internships)
        pd_students, pd_internships = pipeline.clean()


        # 3. Populate the Compatibility Matrix using the cleaned Dataframes 

        # construct the matrix
        columns = pd_internships['internshipID'].tolist()
        index = pd_students['studentID'].tolist()
        matrix = pd.DataFrame(index=index, columns=columns)
        matrix.fillna(value=np.nan, inplace=True)


        # populate the matrix using the compatibility scores between students and internships
        for i in matrix.index.tolist():
            student = pd_students[ pd_students['studentID'] == i]
            for j in matrix.columns.tolist():   
                internship = pd_internships[ pd_internships['internshipID'] == j ]
                matrix.loc[(i, j)] = compute_compatibility(student, internship)



        # 4. Compute Assignments using the Gale-Shapley algorithm

        # if there are no internship or students (or both) left to match do not run the algorithm
        if pd_students.empty or pd_internships.empty:
            pass
        
        else:
            # keeps track of the offers made so far, studentID : (current_internship_offer_ID, [refused_internship_ID1, ...])
            offers = { studentID : [None, []] for studentID in matrix.index.tolist() }

            # keeps track of the number of positions left per job
            available_positions = dict(zip(pd_internships['internshipID'], pd_internships['numberPositions']))

            offers, fulfillments, updated_positions = gale_shapley(offers, matrix, available_positions)

            # format the offers into Student object : Internship object
            offers = { Student.objects.get(studentID=k) : Internship.objects.get(internshipID=v[0]) for k, v in offers.items() if v[0] is not None }

            # write the offers to ComputedMatches table
            for student, internship in offers.items():
                
                # Create an instance of the model with the desired attribute values
                computed_match = ComputedMatch( computedMatchID=f"{student.studentID}{internship.internshipID}", internshipID=internship, studentID=student )

                # save computed match only if not already in comptued matches table
                try:
                    ComputedMatch.objects.get(studentID=student.studentID, internshipID=internship.internshipID)
                    pass
                except:
                    computed_match.save()

            # update the Internships table to reflect the number of positions left per internship after the algorithm has been called
            for id, positions in updated_positions.items():
                internship = Internship.objects.get(internshipID=id)
                internship.numberPositions = positions
                internship.save()

    # show only the computed matches which DO NOT have an interview associated already
    context = { 'computedMatches' : ComputedMatch.objects.filter(interviewID__isnull=True) }

    return render(request, 'algorithm_dashboard.html', context)


# handle the approval routine for a match computed by the algorithm
def approve_match(request, matchID):

    # retrieve the match, the internship listing, the recruiter, the company
    match = ComputedMatch.objects.get(computedMatchID=matchID)

    # create an entry in the Interviews table corresponding to the approved match
    interview = Interview( 
        interviewID=f"Interview_{matchID}", outcome='pending', 
        recruiterID=match.internshipID.recruiterID, studentID=match.studentID, 
        companyID=match.internshipID.companyID, internshipID=match.internshipID
    )

    interview.save()

    # set the computed matches foreign key to the interview ID 
    match.interviewID = interview
    match.save()

    messages.success(request, "successfully saved match and booked internship")
    return redirect('algorithm-dashboard')


# handle the rejection routine for a match computed by the algorithm
def reject_match(request, matchID):

    # retrieve match
    match = ComputedMatch.objects.get(computedMatchID=matchID)

    # return the availablePosition to the match's internship
    internship = Internship.objects.get(internshipID=match.internshipID.internshipID)
    internship.numberPositions += 1
    internship.save()

    # delete the computed match from the table
    match.delete()

    messages.error(request, "match rejected successfully")
    return redirect('algorithm-dashboard')
    

# ======================================================== #
#  Authentication (Login & Signup) and Authorization logic #
# ======================================================== #

# handle the signup routine for a new studen
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

# handle the login of admin using MFA
def admin_login(request):
    return render(request, 'auth/admin_login.html')

# handle the logout routine for all app users
def user_logout(request):
    # logout user in current session
    logout(request)

    messages.success(request, 'logout successfull')  
    return redirect('home')



# ================================================== #
#  Student, Recruiters, and Internships detail pages #
# ================================================== #

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




# =============================================== #
#  Admin Dashboard - Query Database functionality #
# =============================================== #

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
