from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect


# view for the route '/home' 
def home(request):
    return render(request, 'home.html')


def formSuccess(request):
    return render(request, 'form-success.html')

# view for the route '/student'
def student(request):
    # POST request sent on '/student', trigger registration procedure
    if request.method == 'POST':

        # process data and register student to database        

        return redirect('form-success')

    # serve the registration form for new students
    else:
        return render(request, 'student.html')


# view for the route '/internship'
def internship(request):
    # POST request sent on '/internship', trigger registration procedure
    if request.method == 'POST':
        
        # process data and register internship to database

        return redirect("form-success")

    # serve the registration form for new internships
    else:
        return render(request, 'internship.html')