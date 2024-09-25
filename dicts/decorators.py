from functools import wraps

from django.http import HttpResponseForbidden


def permission_required(permission_code, action):
    """
    Decorator to check if the user has the specified permission.
    Usage:
        @check_perms('app_label.permission_codename')
        def my_view(request):
            ...
    """

    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            user = request.user

            has_permission = user.permissions.filter(permission_code=permission_code, action=action).exists()

            if not has_permission:
                return HttpResponseForbidden("You do not have permission to perform this action.")

            return view_func(request, *args, **kwargs)

        return _wrapped_view
    return decorator