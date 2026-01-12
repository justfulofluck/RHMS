from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages

def role_required(*roles):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect('login')
            
            # Allow Superusers to access any role-protected page
            if request.user.is_superuser:
                return view_func(request, *args, **kwargs)

            if hasattr(request.user, 'role') and request.user.role in roles:
                return view_func(request, *args, **kwargs)
            
            # If logged in but wrong role
            messages.error(request, "You do not have permission to access this page.")
            return redirect('homepage')
        return _wrapped_view
    return decorator
