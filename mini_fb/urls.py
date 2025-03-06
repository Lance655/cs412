# File: urls.py
# Author: Lance Sinson (ssinson@bu.edu), 2/21/25
# Description: The urls file for the mini_fb website. 

from django.urls import path
from .views import * # ShowAllProfilesView, ShowProfilePageView, CreateProfileView, CreateStatusMessageView, UpdateProfileView

urlpatterns = [
    path('', ShowAllProfilesView.as_view(), name="show_all_profiles"),
    path('profile/<int:pk>', ShowProfilePageView.as_view(), name="show_profile"),
    path('create_profile', CreateProfileView.as_view(), name="create_profile" ),
    path('profile/<int:pk>/create_status', CreateStatusMessageView.as_view(), name="create_status"),
    path('profile/<int:pk>/update', UpdateProfileView.as_view(), name="update_profile"),
]