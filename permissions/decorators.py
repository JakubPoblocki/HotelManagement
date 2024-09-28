from functools import wraps

from django.http import HttpResponseForbidden


def required_permission(permission_code, action):
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
            permission = user.permissions.filter(permission_code=permission_code)

            if permission is None:
                return HttpResponseForbidden("You do not have permission to perform this action.")

            actions_mapping = {
                'READ': permission.can_read,
                'WRITE': permission.can_write,
                'DELETE': permission.can_delete
            }

            has_permission = actions_mapping.get(action)
            if has_permission is None or not has_permission:
                return HttpResponseForbidden("You do not have permission to perform this action.")

            return view_func(request, *args, **kwargs)

        return _wrapped_view
    return decorator