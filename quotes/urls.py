# File: urls.py
# Author: Lance Sinson (ssinson@bu.edu), 2/7/25
# Description: The urls file for redirecting http requests.

# quotes/urls.py
from django.urls import path

from django.conf import settings
from . import views 

urlpatterns = [
    # path("", home_page_view),
    # path("quote/", ),
    path(r'', views.quote, name="home_page"),
    path(r'quote', views.quote, name="quote"),
    path(r'show_all', views.show_all, name="show_all"),
    path(r'about', views.about, name="about"),
]