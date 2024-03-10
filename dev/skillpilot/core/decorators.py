from django.http import HttpResponse
from django.shortcuts import redirect

# will take the user to the homepage is they are already authorised and try to access login or register pages from url or button
def unauthenticated_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated: # check if authenticated
            return redirect('home')
        else:
            return view_func(request, *args, **kwargs)  # else will run the attached function code 
    
    return wrapper_func

def allowed_users(allowed_roles=[]):
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):

            group = None
            if request.user.groups.exists():
                group = request.user.groups.all()[0].name

            if group in allowed_roles:
                return view_func(request, *args, **kwargs)
            else:
                return redirect('home')
        return wrapper_func
    return decorator
            