# events/models.py

from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.contrib.auth.models import User

class CustomUser(AbstractUser):
    # Inherit fields from AbstractUser, which includes 'username', 'groups', 'user_permissions'
    # You can add additional fields here if needed

    # Example additional fields:
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    bio = models.TextField(blank=True)

    # Use related_name to avoid clashes with the default User model
    groups = models.ManyToManyField(
        Group,
        related_name='customuser_set',  # Change related_name to avoid clash
        blank=True,
        help_text='The groups this user belongs to.',
        related_query_name='customuser',
    )
    
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='customuser_set_permissions',  # Change related_name to avoid clash
        blank=True,
        help_text='Specific permissions for this user.',
        related_query_name='customuser_permissions',
    )

    def __str__(self):
        return self.username

class Event(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    location = models.CharField(max_length=255)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    image = models.ImageField(upload_to='event_images/', blank=True, null=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)

class UserProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    preferred_category = models.CharField(max_length=100, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    location = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.user.username
    
class EventRegistration(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    registered_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'event')  # Prevent duplicate registrations

    def __str__(self):
        return f"{self.user.username} - {self.event.title}"
