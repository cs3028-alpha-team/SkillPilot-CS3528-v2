from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from . models import *
from . forms import *
from django.contrib.auth.forms import UserCreationForm

# view for the route '/home' 
def home(request):
    return render(request, 'home.html')

# render view upon form submission to notify user of success
def formSuccess(request):
    return render(request, 'form-success.html')

def formFailure(request):
    return render(request, 'form-failure.html')

# render view for admin page
@login_required
def admin(request):
    return render(request, 'admin.html')

# Lives in the dashboard app
def dashboard(request):
    return render(request, 'dashboard/dashboard.html')

# render view with admin contact details
def contacts(request):
    return render(request, 'contacts.html')

# render view for login page
def Login(request):
    return render(request, 'Login-page.html')

# render view for registration page
def registration_user(request):
    return render(request, 'student-registration.html')

# render view for registration page
def registration_company2(request):
    return render(request, 'company-registration.html')

# render view for Login page
def employer_Login(request):
    return render(request, 'Login-company.html')

# render view for Login
def login_admin(request):
    return render(request, 'Login-admin.html')

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
@login_required
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
    
 # view to handle login
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
        return render(request, 'Login-page.html')#
    
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
from django.shortcuts import redirect
from django.shortcuts import redirect

def registering_company(request):
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('username')
            messages.success(request, 'Account was created for ' + user)
            return redirect('Login-company')  # Redirect to the Login-company page after successful registration
    else:
        form = UserCreationForm()
    
    context = {'form': form}
    return render(request, 'company-registration.html', context)

