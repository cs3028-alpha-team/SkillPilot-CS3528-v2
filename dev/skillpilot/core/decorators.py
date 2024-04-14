from django.shortcuts import redirect
from functools import wraps


def allowed_users(allowed_roles=[]):
    def decorator(view_func):
        @wraps(view_func)
        def wrapper_func(request, *args, **kwargs):
            group = None
            if request.user.groups.exists():
                group = request.user.groups.first().name

            if group in allowed_roles:
                return view_func(request, *args, **kwargs)
            else:
                return redirect('home')
        return wrapper_func
    return decorator
