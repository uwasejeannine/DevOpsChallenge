from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import UserProfile


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        # Only create if it doesn't exist
        UserProfile.objects.get_or_create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    # Check if profile exists before saving
    try:
        if isinstance(instance, User):
            instance.userprofile.save()
        else:
            instance.save()
    except UserProfile.DoesNotExist:
        UserProfile.objects.create(user=instance)
