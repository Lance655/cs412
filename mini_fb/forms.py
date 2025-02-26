# File: forms.py
# Author: Lance Sinson (ssinson@bu.edu), 2/28/25
# Description: The forms file for the mini_fb website to create a new profile. 

# mini_fb/forms.py
# define the forms that we use for create/update/delete operations

from django import forms
from .models import Profile, StatusMessage

class CreateProfileForm(forms.ModelForm):
    '''A form to add a Profile to the database'''

    class Meta:
        '''Associate this form with a model from out database'''
        model = Profile
        # specify the fields you want to be able to create with this form
        fields = ['first_name', 'last_name', 'city', 'email_address', 'image_url']
