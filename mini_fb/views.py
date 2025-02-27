# File: views.py
# Author: Lance Sinson (ssinson@bu.edu), 2/21/25
# Description: The views file for the mini_fb website. 

# mini_fb/views.py
# views for the mini_fb application
from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView
from .models import Profile, StatusMessage
from .forms import CreateProfileForm, CreateStatusMessageForm
import random
from django.urls import reverse


# Create your views here.
class ShowAllProfilesView(ListView):
    '''Define a view class to show all mini_fb profiles.'''

    model = Profile
    template_name = "mini_fb/show_all_profiles.html"
    context_object_name = "profiles" # note plural variable name

class ShowProfilePageView(DetailView):
    '''Define a view class to show one profile record'''

    model = Profile
    template_name = "mini_fb/show_profile.html"
    context_object_name = "profile" # note singular variable

class CreateProfileView(CreateView):
    '''Define a view class to create a profile'''

    # specify the form class
    form_class = CreateProfileForm
    template_name = "mini_fb/create_profile_form.html"

class CreateStatusMessageView(CreateView):
    '''Define a class to create a status message for a profile'''

    form_class = CreateStatusMessageForm
    template_name = "mini_fb/create_status_form.html"

    def get_context_data(self):
        '''Return the dictionary of context variables for use in the template.'''

        # calling the superclass method
        context = super().get_context_data()

        # find/add the profile to the context data
        # retrieve the PK from the URL pattern
        pk = self.kwargs['pk']
        profile = Profile.objects.get(pk=pk)

        # add this article into the context dictionary:
        context['profile'] = profile
        return context
    
    def form_valid(self, form):
        '''This method attaches the profile primary key to the corresponding status message object's foreign key'''
        pk = self.kwargs['pk']
        profile = Profile.objects.get(pk=pk)
        form.instance.profile = profile

        return super().form_valid(form)

    def get_success_url(self):
        '''Route submitted status forms back to the original profile page'''
        pk = self.kwargs['pk']
        return reverse('show_profile', kwargs={'pk':pk})
