from django.contrib.auth.decorators import user_passes_test
from django.core.exceptions import PermissionDenied

def manager_required(function=None, redirect_field_name=None, login_url=None):
    actual_decorator = user_passes_test(
        lambda u: u.is_active and u.groups.filter(name='Manager').exists(),
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator
