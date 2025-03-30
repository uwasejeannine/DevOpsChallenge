from django.contrib.auth.models import User
from .models import UserProfile
from django.db.models.signals import post_save
from django.dispatch import receiver
import logging

logger = logging.getLogger(__name__)

class UserProfileMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Check if user is authenticated but doesn't have a profile
        if request.user.is_authenticated:
            try:
                # This will raise the exception if no profile exists
                profile = request.user.userprofile
            except User.userprofile.RelatedObjectDoesNotExist:
                # Create a profile if it doesn't exist
                logger.info(f"Creating missing UserProfile for user {request.user.username}")
                UserProfile.objects.create(user=request.user)
        
        response = self.get_response(request)
        return response


# Add signal to create user profile when a user is created
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    # Only create a profile if this is a new user and they don't already have one
    if created:
        try:
            # Check if profile exists first
            instance.userprofile
        except User.userprofile.RelatedObjectDoesNotExist:
            # Only create if it doesn't exist
            UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    # Only save existing profiles, don't create new ones here
    try:
        profile = instance.userprofile
        profile.save()
    except User.userprofile.RelatedObjectDoesNotExist:
        # Don't create a profile here, as it might be handled by create_user_profile
        pass