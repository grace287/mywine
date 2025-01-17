from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission, User
from django.db.models.signals import post_save
from django.dispatch import receiver


class CustomUser(AbstractUser):
    profile_image = models.ImageField(upload_to="profile_images/", blank=True, null=True)
    groups = models.ManyToManyField(
        Group,
        verbose_name='the groups this user belongs to',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name="customuser_set",
    )
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name='specific permissions for this user',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name="customuser_set",
    )

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    profile_image = models.ImageField(upload_to='profile_images/', blank=True, null=True)
    favorite_wine = models.CharField(max_length=100, blank=True)
    price_range = models.CharField(max_length=50, blank=True)
    
    def __str__(self):
        return f'{self.user.username} Profile'
    
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    marketing_agreement = models.BooleanField(default=False)
    terms_agreement_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} UserProfile'
