from django.utils.deprecation import MiddlewareMixin
from django.contrib.auth.models import AnonymousUser

from .models import UserProfile


class UserProfileMiddleware(MiddlewareMixin):
    """
    Middleware to attach UserProfile to authenticated users in request
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Process request
        self.process_request(request)
        
        # Get response
        response = self.get_response(request)
        
        # Return response
        return response

    def process_request(self, request):
        """
        Attach userprofile to authenticated users
        """
        if hasattr(request, 'user') and not isinstance(request.user, AnonymousUser) and request.user.is_authenticated:
            # Get or create user profile
            try:
                # Try to access userprofile
                profile = request.user.userprofile
            except UserProfile.DoesNotExist:
                # Create profile if doesn't exist
                profile = UserProfile.objects.create(user=request.user)
                
        return True