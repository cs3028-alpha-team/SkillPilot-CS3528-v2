from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group, auth
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from . models import *
from . forms import *
from . gale_shapley import *
from . data_pipeline import *
import pickle
import random 
from django.db.models import Q
from .decorators import *
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib
import matplotlib.pyplot as plt
matplotlib.use('Agg') # use the agg backend to silence GUI warning
import io
import base64
from django.db.models import Q
from datetime import date
import random
from django.core.validators import validate_email
from django.core.exceptions import ValidationError



@login_required
@allowed_users(allowed_roles=['Admin']) # access to Admin accounts only    
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
# render home page
def home(request):

    # for it in Internship.objects.all():
    #     it.numberPositions = random.randint(2, 6)
    #     it.save()

    return render(request, 'home.html')

# render contacts page
def contacts(request):
    return render(request, 'contacts.html')

# render help page
def help(request):
    return render(request, 'help.html')

# render error page
def error(request):
    return render(request, 'error.html')

# ============================================== #
#  Student, Recruiter, and Admin Dashboard pages #
# ============================================== #

"""
The dashboard functions control the functionality for the recruiter, student and admin
dashboard pages. 
"""

# view for the route '/student'
@login_required
@allowed_users(allowed_roles=['Students']) # access to student accounts only
def student_dashboard(request):
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            existing_student = Student.objects.filter(email=email).first()
            if existing_student:
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
                existing_student.save()
                messages.success(request, 'Form successful!')
            else:
                form.save()
                messages.success(request, 'Form successful!')
        else:
            messages.error(request, 'Form unsuccessful try again')
        return redirect('student')

    else:
        form = StudentForm()
        context = {'form': form}

    
    try:
        user = request.user
        student_email = user.email
        student_username = user.username
        
        student = get_object_or_404(Student, email=student_email)
        interview = get_object_or_404(Interview, studentID=student.studentID)
        recruiter = get_object_or_404(Recruiter, pk=interview.recruiterID.pk)
        
        start_dt = date.today().replace(day=1, month=1).toordinal()
        end_dt = date.today().toordinal()
        random_date = date.fromordinal(random.randint(start_dt, end_dt))
        modes = ['online', 'in-person']
        random_mode = random.choice(modes)
        
        context = {'interview': interview, 'username': student_username, 'recruiter': recruiter, 'date': random_date, 'mode': random_mode, 'form': form}
        return render(request, 'student_dashboard.html', context)
    
    except Student.DoesNotExist:
        print("Student does not exist")
    
    except Interview.DoesNotExist:
        print("Interview does not exist")
        
    except Recruiter.DoesNotExist:
        print("Recruiter does not exist")

    except Exception as e:
        print("An error occurred:", e)

    return render(request, 'student_dashboard.html', context)         


# Handle recruiters wanting to delete posted internships
@login_required
@allowed_users(allowed_roles=['Companies']) #Access to companies only 
def delete_internship(request, internship_id):
    if request.method == 'POST':
        try:
            internship = Internship.objects.get(pk=internship_id)
            internship.delete()
            return redirect('recruiter')  
        except Internship.DoesNotExist:
            return render(request, 'error.html', context={ 'error': 'Internship does not exist'})

    else:
        return render(request, 'error.html', context={ 'error': 'An error occured'})


# Handle recruiters wanting to update their internships
@login_required
@allowed_users(allowed_roles=['Companies'])  #Access to companies only 
def recruiter_update(request, internship_id):
    internship = get_object_or_404(Internship, pk=internship_id)
    form = InternshipForm(instance=internship)

    if request.method == 'POST':
        form = InternshipForm(request.POST, instance=internship)
        if form.is_valid():
            form.save()
            return redirect('recruiter')  

    return render(request, 'recruiter_update.html', {'form': form, 'internship': internship})

# view for the route '/recruiter'
@login_required
@allowed_users(allowed_roles=['Companies']) 
def recruiter_dashboard(request):
    form = InternshipForm()
    logged_in_recruiter = request.user
    try:
        # Get the logged-in recruiter
        recruiter = Recruiter.objects.get(email=logged_in_recruiter.email)
        #print("Recruiter companyID:", recruiter.companyID)
        
        # Retrieve posted internships associated with the corresponding recruiter
        posted_internships = Internship.objects.filter(recruiterID=recruiter)
        print("Posted internships:", posted_internships)

        # Prepare context data
        context = {'form': form, 'company_id': recruiter.recruiterID, 'posted_internships': posted_internships}
    
        #context = {'form': form, 'company_id': recruiter.recruiterID}
    except Recruiter.DoesNotExist:
        messages.error(request, 'No recruiter associated with the logged-in user')
        return redirect('home')

    if request.method == 'POST':
        form = InternshipForm(request.POST)
        if form.is_valid():
            form.save() 
            messages.success(request, 'Form successful!')
            return redirect('recruiter')
        else:
            messages.error(request, 'Form unsuccessful try again')
            context['form'] = form
            return render(request, 'recruiter_dashboard.html', context)
    else:
        """
        Interview system code, used to display interview details for a recruiter.
        """
        try:
            # Get recruiter details
            user = request.user
            recruiter_email = user.email
            recruiter_username = user.username

            recruiter = get_object_or_404(Recruiter, email=recruiter_email)
            interviews = get_list_or_404(Interview, recruiterID=recruiter.recruiterID)
            students = [get_object_or_404(Student, pk=interview.studentID.pk) for interview in interviews]

            interview_pairs = zip(interviews, students)

            # Generate random date and mode
            start_dt = date.today().replace(day=1, month=1).toordinal()
            end_dt = date.today().toordinal()
            random_date = date.fromordinal(random.randint(start_dt, end_dt))
            modes = ['online', 'in-person']
            random_mode = random.choice(modes)

            return render(request, 'recruiter_dashboard.html', {'interviews': interview_pairs, 'username': recruiter_username, 'date': random_date, 'mode': random_mode, 'form':form })
        
        # deal with exceptions
        except (Interview.DoesNotExist, Student.DoesNotExist):
            print("An object does not exist")
            return render(request, 'recruiter_dashboard.html', context)

        except Exception as e:
            print("An error occurred:", e)
            return render(request, 'recruiter_dashboard.html', context)

        
"""
    update interview is used on the recruiter dashboard to
    change an interview's outcome to accepted, rejected or pending.
"""
# Accept/reject an interview
# Currently only changes outcome in the database#
@login_required
@allowed_users(allowed_roles=['Companies']) #Access to companies only 
def update_interview(request, interview_id):
    if request.method == 'POST':
        new_outcome = request.POST.get('new_outcome')
        interview = Interview.objects.get(interviewID=interview_id)
        interview.outcome = new_outcome
        interview.save()
        
        return redirect('student')
    
@login_required
@allowed_users(allowed_roles=['Admin']) #Access to admin only 
def admin(request):
    return render(request, 'admin.html')


# ============================================================ #
#  Admin Dashboard - Companies Management Tool functionalities #
# ============================================================ #
"""
 The companies management tool is used by the admin to add, search and delete companies.
"""
# handle the companies management tool functionality
@login_required
@allowed_users(allowed_roles=['Admin']) # access to admin only
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


# Handle the procedure to delete a company from the database
@login_required
@allowed_users(allowed_roles=['Admin']) #Access to admin only 
def delete_company(request, companyID):
    # Checkls if the request was POST
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
        #Display success message one all checks are completed succesfully and redirect to manage-companies url
        messages.success(request, 'Company deleted successfully. Please contact the recruiter to inform them of the action')
        return redirect('manage-companies')
    
    return render(request, 'companies_management_tool.html') #render the companies management tool template

# register a new company to the database using the payload from the form submitted from the companies management tool
@login_required
@allowed_users(allowed_roles=['Admin']) #Access to admin only 
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
"""
Functions used in the algorithm dashboard where the admin
can see a list of computed matches and approve or reject them
"""
# render the algorithm dashboard page, where the admin can compute and manage assignments
@login_required
@allowed_users(allowed_roles=['Admin']) #Access to admin only
def algorithm_dashboard(request):

    if request.method == 'POST':

        # 1. Construct the Students and Internships dataframes ===============================================================================================

        """
        As per client requirement, each student should have at most one interview at a time, 
        so the dataframe will be composed of all internships with positions still to be filled in 
        and students with no interviews exclusively
        """
        for it in Internship.objects.all():
            it.numberPositions = random.randint(2, 6)
            it.save()

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


        # 2. Prepare the Dataframes for the matchmaking operation, using the DataPipeline class ===============================================================================================
        pipeline = DataPipeline(pd_students, pd_internships)
        pd_students, pd_internships = pipeline.clean()


        # if there are no internship or students (or both) left to match do not run the algorithm
        if pd_students.empty or pd_internships.empty:
            pass
        
        else:
            # 3. Populate the Compatibility Matrix using the cleaned Dataframes ===============================================================================================

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

            # serialise the matrix, so that it can be used during the classification task at the bottom of this function
            with open('matrix.pkl', 'wb') as file:
                pickle.dump(matrix, file)

            # 4. Compute Assignments using the Gale-Shapley algorithm ===============================================================================================

            # keeps track of the offers made so far, studentID : (current_internship_offer_ID, [refused_internship_ID1, ...])
            offers = { studentID : [None, []] for studentID in matrix.index.tolist() }

            # keeps track of the number of positions left per job
            available_positions = dict(zip(pd_internships['internshipID'], pd_internships['numberPositions']))

            offers, fulfillments, updated_positions, comparisons, time_elapsed = gale_shapley(offers, matrix, available_positions)



            # 5. Assemble the analytics dictionary for this run of the algorithm ===============================================================================================

            # filter all key:value pairs from the offers dictionary which are not None, i.e. all students with an offer
            nonNull_offers = { k:v for k,v in offers.items() if v[0] is not None}

            # create a lineplot instance of the number of internships to be assigned at each iteration of the algorithm
            fulfillments_df = pd.DataFrame({'algorithm_iterations': range(1, len(fulfillments) + 1), 'internships_to_be_assigned': fulfillments[::-1]})
            fulfillments_chart = sns.lineplot(data=fulfillments_df, x='algorithm_iterations', y='internships_to_be_assigned', color='#2d00f7')
            fulfillments_chart.set_xlabel('Algorithm Iterations')
            fulfillments_chart.set_ylabel('Internships to be Assigned')
            fulfillments_chart.set_title('Internships to be Assigned vs Algorithm Iterations')
            fig = fulfillments_chart.get_figure()
            fig.set_size_inches(6, 4)


            metrics = {
                'time_elapsed' : f"{time_elapsed} seconds",
                'comparisons_made' : comparisons,
                'students_matched' : f"{round(len(nonNull_offers)/len(offers) * 100, 1)} %",
                'internships_matched' : f"{round(len(columns)* 100 / len(nonNull_offers), 1)} %",
            }


            # compute a dictionary to store all the analytics relevant to the current algorithm run - this is updated at each run
            algorithm_analytics = {
                'metrics' : metrics,
                'assignmentsLeft_vs_iterations_plot' : fulfillments_chart
            }

            # serialise the dictionary so that it can be rendered during GET requests to the analytics dashboard
            with open('algorithm_analytics.pkl', 'wb') as file:
                pickle.dump(algorithm_analytics, file)



            # 6. save database state after algorithm run ===============================================================================================

            # format the offers into Student object : Internship object
            offers = { Student.objects.get(studentID=k) : Internship.objects.get(internshipID=v[0]) for k, v in offers.items() if v[0] is not None }

            # write the offers to ComputedMatches table
            for student, internship in offers.items():
                
                # Create an instance of the model with the desired attribute values
                computed_match = ComputedMatch( computedMatchID=f"{student.studentID}{internship.internshipID}", internshipID=internship, studentID=student )

                # save computed match only if not already in comptued matches table
                try: match_exists = ComputedMatch.objects.get(computedMatchID=f"{student.studentID}{internship.internshipID}")
                except: computed_match.save()

            # update the Internships table to reflect the number of positions left per internship after the algorithm has been called
            for id, positions in updated_positions.items():
                internship = Internship.objects.get(internshipID=id)
                internship.numberPositions = positions
                internship.save()



    # deserialise the trained model and run an assessment on it
    with open('classifier.pkl', 'rb') as f:
        classifier = pickle.load(f)
    classifier.assess()

    # deserialise the matrix from the last run of the algorithm. This approach works since we assume that the last call of the  
    # algorithm used the same dataframes used to compute this matrix
    with open('matrix.pkl', 'rb') as file:
        matrix = pickle.load(file)

    # show only the computed matches which DO NOT have an interview associated already
    matches = ComputedMatch.objects.filter(interviewID__isnull=True)

    # constuct a dataframe to be fed into the classification model
    matches_df_data = []
    for match in matches:

        # fetch the student and internship objects involved in the computed match
        student = Student.objects.get(studentID=match.studentID.studentID)
        internship = Internship.objects.get(internshipID=match.internshipID.internshipID)

        # compute dataframe features
        studentGPA = student.GPA
        internshipGPA = internship.minGPA
        GPADifference = abs(studentGPA - internshipGPA)/100
        fieldExperienceRelevance = round(random.random(), 2) # random between 0.0 and 1.0, in future improvement will be able to calculate relevance based on actual inputs
        contractModeCompatibility = 1 if student.studyMode == internship.contractMode else random.random() * 0.5
        contractPatternCompatibility = 1 if student.studyPattern == internship.contractPattern else random.random() * 0.5
        compatibilityScore = matrix.loc[student.studentID, internship.internshipID]

        row = [ studentGPA, internshipGPA, compatibilityScore, GPADifference, fieldExperienceRelevance, contractModeCompatibility, contractPatternCompatibility ]
        matches_df_data.append(row)

    matches_df = pd.DataFrame(data=matches_df_data, columns=['studentGPA', 'internshipGPA', 'compatibilityScore', 'GPADifference', 'fieldExperienceRelevance', 'contractModeCompatibility', 'contractPatternCompatibility'])
    
    # compute the classification output for each match and attach it to the computedMatch object
    predictions = classifier.predict(matches_df)
    for i in range(len(matches)): matches[i].label = predictions[i]

    # format the computedMatches and label them using the pre-trained classifier 
    context = { 'computedMatches' : matches }

    return render(request, 'algorithm_dashboard.html', context)


"""
    Approve_match is used to approve a computed match
"""
# handle the approval routine for a match computed by the algorithm
@login_required
@allowed_users(allowed_roles=['Admin']) #Access to admin only 
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

"""
    Reject_match is used to reject a computed match
"""
# handle the rejection routine for a match computed by the algorithm
@login_required
@allowed_users(allowed_roles=['Admin']) #Access to admin only 
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
    


# ===================================== #
# Admin Dashboard - Analytics Dashboard #
# ===================================== #
"""
    Analytics dashboard is used by the admin to display various analytics
    about students, internships computed matches in the form of charts and heatmaps
"""
@login_required
@allowed_users(allowed_roles=['Admin']) #Access to admin only 
def analytics_dashboard(request):

    context = {}
    buffer = io.BytesIO()

    # calculate system-generic stats
    students_count = len(Student.objects.all())
    internships_count = len(Internship.objects.all())
    recruiters_count = len(Recruiter.objects.all())
    companies_count = len(Company.objects.all())

    context['general'] = { 
        'students_count' : students_count, 
        'internships_count' : internships_count, 
        'recruiters_count' : recruiters_count, 
        'companies_count' : companies_count, 
    }

    # generate a student dataframe to develop the charts 
    students = [ [student.studentID, student.currProgramme, student.studyMode, student.studyPattern] for student in Student.objects.all() ]
    students_df = pd.DataFrame(data=students, columns=['studentID', 'currProgramme', 'studyMode', 'studyPattern'])

    # generate an internship dataframe to develop the charts 
    internships = [ [ internship.internshipID, internship.contractMode, internship.contractPattern, internship.field, internship.numberPositions ] for internship in Internship.objects.all() ]
    internships_df = pd.DataFrame(data=internships, columns=['internshipID', 'contractMode', 'contractPattern', 'field', 'numberPositions'])


    # 1. Piechart for distribution of students by studyPattern =================================================================================

    # group and count students by studyPattern and studyMode columns in the dataframe
    studyPattern_counts = students_df['studyPattern'].value_counts()
    studyMode_counts = students_df['studyMode'].value_counts()

    # plot the piechart to be display and declare settings
    fig, ax = plt.subplots(figsize=(4, 3))
    ax.pie(studyPattern_counts, labels=studyPattern_counts.index, autopct='%1.1f%%', startangle=90, colors=['#4793AF', '#DD5746'])
    ax.axis('equal')
    ax.set_title('Distribution of students by Study Pattern')

    # save the studyPattern chart and uncode it using binary stream
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    studyPattern_chart = base64.b64encode(buffer.getvalue()).decode('utf-8')
    plt.close()

    # set the context dictionary entry so that other charts can be computed 
    context['studyPattern_chart'] = studyPattern_chart


    # 2. Piechart for distribution of students by studyMode =====================================================================================

    # plot the piechart to be display and declare settings
    fig, ax = plt.subplots(figsize=(4, 3))
    ax.pie(studyMode_counts, labels=studyMode_counts.index, autopct='%1.1f%%', startangle=90, colors=['#ed6a5a', '#f4f1bb', '#9bc1bc'])
    ax.axis('equal')
    ax.set_title('Distribution of students by Study Mode')

    # save the studyPattern chart and uncode it using binary stream
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    studyMode_chart = base64.b64encode(buffer.getvalue()).decode('utf-8')
    plt.close()

    # set the context dictionary entry so that other charts can be computed 
    context['studyMode_chart'] = studyMode_chart


    # 3. Piechart for distribution of internships by contractMode =================================================================================

    # group and count internships by contractPattern and contractMode columns in the dataframe
    contractPattern_counts = internships_df['contractPattern'].value_counts()
    contractMode_counts = internships_df['contractMode'].value_counts()

    # plot the piechart to be display and declare settings
    fig, ax = plt.subplots(figsize=(4, 3))
    ax.pie(contractPattern_counts, labels=contractPattern_counts.index, autopct='%1.1f%%', startangle=90, colors=['#f6f7eb', '#e94f37'])
    ax.axis('equal')
    ax.set_title('Distribution of internships by Contract Pattern')

    # save the studyPattern chart and uncode it using binary stream
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    contractPattern_chart = base64.b64encode(buffer.getvalue()).decode('utf-8')
    plt.close()

    # set the context dictionary entry so that other charts can be computed 
    context['contractPattern_chart'] = contractPattern_chart

    # 4. Piechart for distribution of internships by contractPattern ==============================================================================
    
    # plot the piechart to be display and declare settings
    fig, ax = plt.subplots(figsize=(4, 3))
    ax.pie(contractMode_counts, labels=contractMode_counts.index, autopct='%1.1f%%', startangle=90, colors=['#124e78', '#f0f0c9', '#f2bb05'])
    ax.axis('equal')
    ax.set_title('Distribution of internships by Contract Mode')

    # save the studyPattern chart and uncode it using binary stream
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    contractMode_chart = base64.b64encode(buffer.getvalue()).decode('utf-8')
    plt.close()

    # set the context dictionary entry so that other charts can be computed 
    context['contractMode_chart'] = contractMode_chart



    # 5. Last computed compatibility matrix in the form of a heatmap ==============================================================================
    with open('matrix.pkl', 'rb') as file:
        matrix = pickle.load(file)

    fig, ax = plt.subplots(figsize=(9, 7))
    sns.heatmap(matrix.iloc[:15, :15], cmap="viridis", annot=True, linewidth=.5)  # Sample 20 rows for the heatmap
    ax.set_title('Last computed Compatibility Matrix sample')
    plt.xticks(rotation=45, ha='right')
    plt.yticks(rotation=45, ha='right')
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    matrixChart = base64.b64encode(buffer.getvalue()).decode('utf-8')
    plt.close()
    context['matrix_chart'] = matrixChart


    # 6. Histogram of students grouped by current programme

    # run a value count, and display in the form of a table on the screen
    currProgramme_counts = students_df['currProgramme'].value_counts().reset_index()
    currProgramme_counts.columns = ['Programme of Study', 'Students Enrolled']
    context['currProgramme_df'] = currProgramme_counts.to_html(classes='table table-bordered table-striped', index=False)


    # 7. Analytics specific to the last algorithm run ===============================================================

    with open('algorithm_analytics.pkl', 'rb') as file:
        analytics_dictionary = pickle.load(file)

    # encode the analytics chart into a binary stream
    chart = analytics_dictionary['assignmentsLeft_vs_iterations_plot']
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    algorithm_chart = base64.b64encode(buffer.getvalue()).decode('utf-8')
    plt.close()
    analytics_dictionary['assignmentsLeft_vs_iterations_plot'] = algorithm_chart

    context['algorithm_analytics'] = analytics_dictionary



    # 8. Histogram of total internship positions per Field

    # create an internship dataframe with internship field and positions, 
    # then run a value count on that and display the dataframe to screen, in the form of a table
    total_positions_df = internships_df[['field', 'numberPositions']]
    positions_per_field = total_positions_df.groupby('field')['numberPositions'].sum().reset_index()
    positions_per_field.columns = ['Internship Field', 'Available Internships']
    context['positionsPerField_df'] = positions_per_field.to_html(classes='table table-bordered table-striped', index=False)

    return render(request, 'analytics_dashboard.html', context)



# ======================================================== #
#  Authentication (Login & Signup) and Authorization logic #
# ======================================================== #

# Handle the signup routine for a new studen
def student_signup(request):
    if request.user.is_authenticated: # Checks if user is authenticated 
        return redirect('student') # If true sends them to the student dashboard
    if request.method == 'POST': # When the sign up is submitted 
        # The below information is collected
        username = request.POST.get('studentUsername') 
        email = request.POST.get('studentEmail')
        password1 = request.POST.get('studentPassword1')
        password2 = request.POST.get('studentPassword2')

        #Check if the email submitted has the correct format
        try:
            validate_email(email) #using djanos validate email function 
        except ValidationError:
            #if email is incorrect print error message
            messages.error(request, 'Please enter a valid email address.') 
            return render(request, 'auth/student_signup.html')
        
        # Check if username already exists, if true sends an error message 
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists. Please choose a different username.')
            return render(request, 'auth/student_signup.html')

        # Check if email already exists, if true sends an error message 
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists. Please use a different email address.')
            return render(request, 'auth/student_signup.html')

        # Check if passwords match, if true sends an error message 
        if password1 != password2:
            messages.error(request, 'Passwords do not match.')
            return render(request, 'auth/student_signup.html')

        # Create new user if all checks pass, with the values collected from the submitted form 
        new_user = User.objects.create_user(username=username, email=email, password=password1)
        group = Group.objects.get(name='Students')
        new_user.groups.add(group) #Assigns the user to group student 

        messages.success(request, 'Signup successful!')
        return redirect('student-login')

    return render(request, 'auth/student_signup.html')


# Handle the login routine for a returning student
def student_login(request):
    if request.user.is_authenticated: # If user it authenticated 
        return redirect('student')# Send them to student dashboard 
    form = UserLoginForm() # If not authenticated, create a form for user login
    # Check if the request method is POST e.g. form submitted 
    if request.method == 'POST':
        # bind the form with the POST data
        form = UserLoginForm(request, data=request.POST)

        if form.is_valid(): # Checks if the form is valid 
            username = request.POST.get('username') # Collects the username 
            password = request.POST.get('password') # Collects the password 
            # Authenciate the user 
            user = authenticate(request, username=username, password=password)

            if user is not None: #Checks if authentication is successful
                auth.login(request, user) # If passed, logs the user in
                messages.success(request, 'login successfull')  # Prints success message 
                return redirect('student') # Send the user to the student dashboard 

        else:    # If the form is invalid, print error message and send user to sign up page   
            messages.error(request, 'Login failed! please try again or signup for an account') 
            return redirect('student-signup')

    return render(request, 'auth/student_login.html') # Render the login page 

# Handle the signup routine for new recruiters
def recruiter_signup(request):
    if request.user.is_authenticated: # Checks if user if authenticated 
        return redirect('recruiter') # If authenticated, send to recruiter dashboard 
    # Check if the request method is POST e.g. form submitted 
    if request.method == 'POST':
        # values are extracted from the recruiter sign up form 
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
        # If the companyID is invalid, display an error message and redirect to sign up page
        except Company.DoesNotExist:
            messages.error(request, 'Invalid recruiter token. Please enter a valid recruiter token.')
            return redirect('recruiter-signup')
        
        #Check if the email submitted has the correct format
        try:
            validate_email(recruiter_email) #using djanos validate email function 
        except ValidationError:
            #if email is incorrect print error message
            messages.error(request, 'Please enter a valid email address.') 
            return render(request, 'auth/recruiter_signup.html')
        
        # Check if passwords match
        if password1 != password2:
            messages.error(request, 'Passwords do not match.')
            return redirect('recruiter-signup')

        # Check if the username already exists
        if User.objects.filter(username=recruiter_username).exists():
            messages.error(request, 'Username already exists. Please choose a different username.')
            return redirect('recruiter-signup')
        
        # Check if the recruiterID exits 
        if Recruiter.objects.filter(recruiterID=recruiter_id).exists():
            messages.error(request, 'Recruiter ID already exists. Please choose a different recruiter ID.')
            return redirect('recruiter-signup')
        
        # Check if email already exists, if true sends an error message 
        if User.objects.filter(email=recruiter_email).exists():
            messages.error(request, 'Email already exists. Please use a different email address.')
            return render(request, 'auth/recruiter_signup.html')
        
        # Create the recruiter account if all validations pass, using the calues from the form 
        user = User.objects.create_user(username=recruiter_username, email=recruiter_email, password=password1)
        group = Group.objects.get(name = 'Companies') 
        user.groups.add(group) # makes user group companies 
        # Create a recruiter with the detailts from the form 
        recruiter = Recruiter.objects.create(
            fullName=user.username, 
            email=user.email,  
            recruiterID=recruiter_id,
            companyID=company,
            jobTitle=recruiter_job_title
        )
        # Display a success message, and send user to login page
        messages.success(request, 'Recruiter account created successfully. Please login.')
        return redirect('recruiter-login')

    return render(request, 'auth/recruiter_signup.html') # render recruiter sign up page 

# Handle the login routine for returning recruiters
def recruiter_login(request):
    if request.user.is_authenticated: # Check if the user is authenticated 
        return redirect('recruiter') # If authenticated, send to recruiter dashboard 
    # Check if the request method is POST e.g. form submitted 
    if request.method == 'POST':
        # Values are extracted from the login from 
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        # If the user is authenticated, log them in and redirect to the recruiter form page
        if user is not None:
            login(request, user)
            return redirect('recruiter')  
        # If authentication fails, display an error message and send user back to login page
        else:
            messages.error(request, 'Invalid username or password.')
            return redirect('recruiter-login') 
    
    return render(request, 'auth/recruiter_login.html') # Render recruietr login page

# handle the login of admin using MFA
def admin_login(request):
    return render(request, 'auth/admin_login.html')

# handle the logout routine for all app users
def user_logout(request):
    # logout user in current session
    logout(request)
    # Dislay success message, and send them to home page 
    messages.success(request, 'logout successfull')  
    return redirect('home')



# ================================================== #
#  Student, Recruiters, and Internships detail pages #
# ================================================== #
"""
    The details pages are used to display a list of details about
    a particular student, recruiter or internship.
"""

# Render a given student profile's details page
@login_required
@allowed_users(allowed_roles=['Admin', 'Students', 'Companies']) 
def student_details(request, studentID):
    # Using the studentID passed to retrieve the corresponding student object 
    try:
        student = Student.objects.get(studentID = studentID)
        # Render the student details page with the student object in the context
        return render(request, 'student_details.html', context={ 'student' : student })
    except:
        # If no student is found with the passed studentID, an error message will display 
        messages.error(request, 'Looks like no student with that ID exists!')
        return redirect('query-students')

# render a given recruiter profile's details page
@login_required
@allowed_users(allowed_roles=['Admin', 'Students', 'Companies']) 
def recruiter_details(request, recruiterID):
    # Using the recruiterID passed to retrieve the corresponding recruiter object 
    try:
        recruiter = Recruiter.objects.get(recruiterID = recruiterID)
        # Get the company associated with the recruiter
        # If not found there is a 404 error
        company = get_object_or_404(Company, pk=recruiter.companyID.pk)
         # Render the recruiter details page with the recruiter and company objects in the context
        return render(request, 'recruiter_details.html', context={ 'recruiter' : recruiter, 'company' : company.companyName })
    except:
        # If no recruiter is found with the passed recruiterID, an error message will display 
        messages.error(request, 'Looks like no recruiter with that ID exists!')
        return redirect('query-recruiters')

# render a given live internship's details page
@login_required
@allowed_users(allowed_roles=['Admin', 'Students', 'Companies']) 
def internship_details(request, internshipID):
    # Using the internshipID passed to retrieve the corresponding internship object 
    try:    
        internship = Internship.objects.get(internshipID = internshipID)
        # Get the company and recruiter associated with the inetrnship 
        # If not found there is a 404 error
        company = get_object_or_404(Company, pk=internship.companyID.pk)
        recruiter = get_object_or_404(Recruiter, pk=internship.recruiterID.pk)

        # Render the internship details page with the internship, recruiter and company objects in the context
        return render(request, 'internship_details.html', context={ 'internship' : internship, 'recruiter' : recruiter.fullName, 'company': company.companyName })
    except:
        # If no internship is found with the passed internshipID, an error message will display 
        messages.error(request, 'Looks like no internship with that ID exists!')
        return redirect('query-internships')




# =============================================== #
#  Admin Dashboard - Query Database functionality #
# =============================================== #

"""
    The query database functions are used to search the
    student, recruiter and internship tables, and display a
    list of search results.
"""

# handle the routine triggered from the admin dashboard to query all student profiles
@login_required
@allowed_users(allowed_roles=['Admin']) #Access to admin only 
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

@login_required
@allowed_users(allowed_roles=['Admin']) #Access to admin only 
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
@login_required
@allowed_users(allowed_roles=['Admin']) #Access to admin only 
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

#download query results as a csv file
def download_csv(data, filename):
    df = pd.DataFrame(data)

    # Create CSV file
    csv_file = df.to_csv(index=False)

    response = HttpResponse(csv_file, content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="{filename}.csv"'

    return response

#download recruiters
def download_recruiters_csv(request):
    recruiters = Recruiter.objects.all()
    response = download_csv(recruiters.values(), 'recruiter_search_results')
    return response

#download students
def download_students_csv(request):
    students = Recruiter.objects.all()
    response = download_csv(students.values(), 'student_search_results')
    return response

#download internships
def download_internships_csv(request):
    internships = Recruiter.objects.all()
    response = download_csv(internships.values(), 'internship_search_results')
    return response

# ========================================= Recruiter and internship delete function ============================================ #

# handle the procedure to delete a student from the database
@login_required
@allowed_users(allowed_roles=['Students']) # Access to students only 
def delete_user(request):
    # Checks if the request is post
    if request.method == 'POST':
        user = request.user # Get the currently logged in user 

        # Delete all student objects connected to the user email 
        Student.objects.filter(email=user.email).delete()

        # Delete the user
        user.delete()

        # Log the user out 
        logout(request)
        # Display a success message
        messages.success(request, 'Student account deleted successfully')
        return redirect('home') # Direct the user home 
    else:
        return redirect('home') # If the request is instead get, direct the user home without deleting any forms 

# Handle the procedure to delete a recruiter from the database
@login_required
@allowed_users(allowed_roles=['Companies']) #Access to companies only 
def delete_recruiter(request):
    if request.method == 'POST':
        # Get the logged in user 
        logged_in_user = request.user
        
        try:
            # Retrieve the recruiter connected with the logged in user
            recruiter = Recruiter.objects.get(email=logged_in_user.email)
        except Recruiter.DoesNotExist:
            # If there is no recruiter is associated with the logged in user, display message and redirect to the home page
            messages.error(request, 'No recruiter associated with the logged-in user')
            return redirect('home')

        # Store the recruiter email 
        recruiter_email = recruiter.email

        print("Recruiter:", recruiter) # Debugging
        print("Recruiter Email:", recruiter_email) # Debugging

        # Delete the recruiter account associated with the current company
        try:
            recruiter.delete() # Delete recruiter 
            print("Recruiter deleted successfully") #Debugging
        except Exception as e:
            return render(request, 'error.html', context={ 'error': 'Exception occured while deleting Recruiter account'})


        # Delete any internship listings associated with the company
        try:
            Internship.objects.filter(recruiterID=recruiter.recruiterID).delete()

            print("Internships deleted successfully") #Debugging
        except Exception as e:
            return render(request, 'error.html', context={ 'error': 'Exception occured while deleting Internship'})


        # Delete the user associated with the company by email
        if recruiter_email:
            try:
                user = User.objects.get(email=recruiter_email)
                user.delete()
                print("User deleted successfully") # Debugging
            except Exception as e:
                print("Error deleting user:", e) # Debugging

        #Display success message one all checks are completed succesfully, logout the user and redirect to home page
        messages.success(request, 'Company deleted successfully. Please contact the recruiter to inform them of the action')
        logout(request)
        return redirect('home') 
    else:
        #If the request is get, send the user home without deleting any data
        return redirect('home')
    
"""
    Send email is used to send an email to students and recruiters
    to inform them that they have been matched.
    
"""
# function to send an email    
def send_email(request): 
    internships = Internship.objects.all() #get data from database
    students = Student.objects.all()
    recruiters = Recruiter.objects.all()
        
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

