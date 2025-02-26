# File: views.py
# Author: Lance Sinson (ssinson@bu.edu), 2/21/25
# Description: The views file for the mini_fb website. 

# mini_fb/views.py
# views for the mini_fb application
from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView
from .models import Profile, StatusMessage
from .forms import CreateProfileForm
import random

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