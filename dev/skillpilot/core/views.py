from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from . models import *
from . forms import *

# view for the route '/home' 
def home(request):
    return render(request, 'home.html')

# render view upon form submission to notify user of success
def formSuccess(request):
    return render(request, 'form-success.html')

def formFailure(request):
    return render(request, 'form-failure.html')

# render view for admin page
def admin(request):
    return render(request, 'admin.html')

# render view with admin contact details
def contacts(request):
    return render(request, 'contacts.html')

# view for the route '/student'
def student(request):

    form = StudentForm()
    context = { 'form' : form }

    # POST request sent on '/student', trigger registration procedure
    if request.method == 'POST':

        form = StudentForm(request.POST)

        # process data and register student to database

        if form.is_valid():
            form.save() 
            return redirect('form-success')

        else:
            return redirect('form-failure')

    # serve the registration form for new students
    else:
        return render(request, 'student.html', context)

# view for the route '/internship'
def internship(request):

    form = InternshipForm()
    context = { 'form' : form }

    # POST request sent on '/internship', trigger registration procedure
    if request.method == 'POST':
        
        # process data and register internship to database
        form = InternshipForm(request.POST)

        if form.is_valid():

            # create an instance of internship Model
            internship = form.save(commit=False)

            # obtain the Model instances for Recruiter and Company
            companyID = Company.objects.get(id='c1')
            recruiterID = Recruiter.objects.get(id='r1')

            # manually set the company ID and recruiter ID for now
            # but in the future these will be dynamically acquired by checking the user logged-in session
            internship.companyID = companyID
            internship.recruiterID = recruiterID

            form.save() 
            return redirect('form-success')

        else:
            return redirect('form-failure')

    # serve the registration form for new internships
    else:
        return render(request, 'internship.html', context)

# view to render the details of a specific internship opportunity
def internshipDetails(request):
    
    form = InternshipForm()
    context = { 'form' : form }

    # ============================================ EDIT INTERNSHIP LISTING =========================================
    # POST request sent on '/internship', trigger registration procedure
    if request.method == 'POST':
        
        # process data and register internship to database
        form = InternshipForm(request.POST)

        if form.is_valid():

            # update the internship with ID of internshipID using the request payload 

            form.save() 
            return redirect('form-success')

        else:
            return redirect('form-failure')

    # serve the registration form for new internships
    else:
        return render(request, 'internship-details.html', context)