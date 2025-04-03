from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from booking.models import UserProfile


class Command(BaseCommand):
    help = 'Creates UserProfile objects for any User without one'

    def handle(self, *args, **options):
        users_without_profiles = []
        for user in User.objects.all():
            try:
                # Access the userprofile to see if it exists
                user.userprofile
            except User.userprofile.RelatedObjectDoesNotExist:
                users_without_profiles.append(user)
        
        if not users_without_profiles:
            self.stdout.write('All users already have profiles')
            return True
            
        count = 0
        for user in users_without_profiles:
            UserProfile.objects.create(user=user)
            self.stdout.write(f' - Created profile for {user.username}')
            count += 1
        
        self.stdout.write(f'Created {count} user profiles')
        return True