from functools import wraps

from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect


def anonymous_required(func):
    @wraps(func)
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('profile')
        return func(request, *args, **kwargs)
    return wrapper


def group_required(group_name):
    def decorator(func):
        @wraps(func)
        def wrapper(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect('/login/')
            if not request.user.groups.filter(name=group_name).exists():
                raise PermissionDenied(f'You must be in the {group_name} group')
            return func(request, *args, **kwargs)
        return wrapper
    return decorator