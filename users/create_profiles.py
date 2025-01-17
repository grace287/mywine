from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from users.models import Profile

class Command(BaseCommand):
    help = 'Creates profiles for users that do not have one'

    def handle(self, *args, **options):
        users_without_profile = User.objects.filter(profile__isnull=True)
        for user in users_without_profile:
            Profile.objects.create(user=user)
            self.stdout.write(f'Created profile for user: {user.username}')