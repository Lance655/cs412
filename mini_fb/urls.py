# File: urls.py
# Author: Lance Sinson (ssinson@bu.edu), 2/21/25
# Description: The urls file for the mini_fb website. 

from django.urls import path
from .views import ShowAllProfilesView

urlpatterns = [
    path('', ShowAllProfilesView.as_view(), name="show_all_profiles"),
]