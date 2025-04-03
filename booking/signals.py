from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import UserProfile


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created or not hasattr(instance, 'userprofile'):
        UserProfile.objects.get_or_create(user=instance)
    return True


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, raw=False, **kwargs):
    if raw:
        UserProfile.objects.get_or_create(user=instance)
        return True
    
    if hasattr(instance, 'userprofile'):
        instance.userprofile.save()
    else:
        UserProfile.objects.create(user=instance)
    return True