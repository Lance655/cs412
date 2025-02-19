# mini_fb/models.py
# define data models for the mini_fb application

from django.db import models

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