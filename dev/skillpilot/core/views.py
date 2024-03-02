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