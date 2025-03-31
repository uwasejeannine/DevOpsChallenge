# Create this file at your_app/management/commands/create_user_profiles.py
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from booking.models import UserProfile  # Replace with your app name


class Command(BaseCommand):
    help = "Create UserProfile for users who do not have one"

    def handle(self, *args, **kwargs):
        users_without_profile = []

        for user in User.objects.all():
            try:
                user.userprofile
            except User.userprofile.RelatedObjectDoesNotExist:
                users_without_profile.append(user)
                UserProfile.objects.create(user=user)

        if users_without_profile:
            self.stdout.write(
                self.style.SUCCESS(
                    f"Created {len(users_without_profile)} user profiles"
                )
            )
            for user in users_without_profile:
                self.stdout.write(f" - Created profile for {user.username}")
        else:
            self.stdout.write(self.style.SUCCESS("All users already have profiles"))
