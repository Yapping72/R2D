from django.http import HttpResponseForbidden

"""
Middleware that limits the access of staff users to the admin page
"""
class BlockStaffFromAdminMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = request.user
        # Check if the user is staff but not a superuser
        if user.is_authenticated and user.is_staff and not user.is_superuser:
            # If the path starts with /admin/ and is not the login page, block access
            if request.path.startswith('/admin/') and not request.path == '/admin/login/':
                return HttpResponseForbidden("You do not have permission to access this page. Try to login again.")
        return self.get_response(request)