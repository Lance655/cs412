# File: forms.py
# Author: Lance Sinson (ssinson@bu.edu), 3/28/25
# Description: The forms file for the mini_fb website to create a new profile. 

# mini_fb/forms.py
# define the forms that we use for create/update/delete operations

from django import forms
from .models import Profile, StatusMessage

class CreateProfileForm(forms.ModelForm):
    '''A form to add a Profile to the database'''

    class Meta:
        '''Associate this form with a model from our database'''
        model = Profile
        # specify the fields you want to be able to create with this form
        fields = ['first_name', 'last_name', 'city', 'email_address', 'image_url']

class CreateStatusMessageForm(forms.ModelForm):
    '''A form to add a status message to the database'''

    class Meta:
        '''Associate this form with a model from our database'''
        model = StatusMessage
        fields = ['message']

class UpdateProfileForm(forms.ModelForm):
    '''A form to update a Profile from the database'''

    class Meta:
        '''Associate this form with a model from our database'''
        model = Profile
        fields = ['city','email_address','image_url']

class UpdateStatusMessageForm(forms.ModelForm):
    '''A form to update a status message from the database'''

    class Meta:
        '''Associate this form with a model from our database'''
        model = StatusMessage
        fields = ['message']

        