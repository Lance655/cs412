# mini_fb/models.py
# define data models for the mini_fb application

from django.db import models
from django.urls import reverse


# Create your models here.
class Profile(models.Model):
    '''Encapsulate the data profile for each user'''
    first_name = models.TextField(blank=True)
    last_name = models.TextField(blank=True)
    city = models.TextField(blank=True)
    email_address = models.TextField(blank=True)
    image_url = models.URLField(blank=True)

    def __str__(self): 
        '''return a string representation of this model instance.'''
        return f'{self.first_name}'

    def get_status_messages(self):
        '''Return a QuerySet of status messages about this profile.'''
        status_messages = StatusMessage.objects.filter(profile=self)
        return status_messages 

    def get_absolute_url(self):
        '''Return a URL to display one instance of this object.'''
        return reverse('show_profile', kwargs={'pk': self.pk})
    

class StatusMessage(models.Model):
    '''Encapsulate the idea of a status message for a individual profile'''

    # data attributes for Status Messages:
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    message = models.TextField(blank=False)
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        '''return a string representation of this model instance.'''
        return f'{self.message} - {self.profile.first_name}'