# File: urls.py
# Author: Lance Sinson (ssinson@bu.edu), 2/21/25
# Description: The urls file for the mini_fb website. 

from django.urls import path
from .views import ShowAllProfilesView, ShowProfilePageView, CreateProfileView

urlpatterns = [
    path('', ShowAllProfilesView.as_view(), name="show_all_profiles"),
    path('profile/<int:pk>', ShowProfilePageView.as_view(), name="show_profile"),
    path('create_profile', CreateProfileView.as_view(), name="create_profile" ),
]