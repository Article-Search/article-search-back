from functools import wraps
from django.http import JsonResponse
from .models import User
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

def role_required(required_roles):
    # Convert single role to a list for consistency
    if not isinstance(required_roles, list):
        required_roles = [required_roles]

    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            # Check if the user is authenticated
            auth = TokenAuthentication()
            try:
                user_auth_tuple = auth.authenticate(request)
                if user_auth_tuple is not None:
                    request.user, request.auth = user_auth_tuple
            except:
                return JsonResponse({'message': "Authentication failed"}, status=401)

            # Check if the user has the right permissions
            perm = IsAuthenticated()
            if not perm.has_permission(request, view_func):
                return JsonResponse({'message': "You don't have permission to access this route"}, status=403)

            # Check if the user has at least one of the required roles
            if request.user.role in [role_num for role_num, role_name in User.ROLE_CHOICES if role_name in required_roles]:
                return view_func(request, *args, **kwargs)
            else:
                return JsonResponse({'message': "You don't have permission to access this route"}, status=403)

        return _wrapped_view

    return decorator
