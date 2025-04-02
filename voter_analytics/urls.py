# File: urls.py
# Author: Lance Sinson (ssinson@bu.edu), 4/4/25
# Description: The urls file for the voter_analytics website. 

from django.urls import path
from . import views 

urlpatterns = [
    # map the URL (empty string) to the view
	path(r'', views.ShowAllVoters.as_view(), name='voters'),
    path(r'voter/<int:pk>', views.ShowVoter.as_view(), name="voter"),
]