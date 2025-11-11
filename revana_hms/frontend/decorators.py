from functools import wraps
from django.shortcuts import redirect

def role_required(*roles):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if hasattr(request.user, 'role') and request.user.role in roles:
                return view_func(request, *args, **kwargs)
            return redirect('login')  # or show error page
        return _wrapped_view
    return decorator
