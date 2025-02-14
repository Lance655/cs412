# File: urls.py
# Author: Lance Sinson (ssinson@bu.edu), 2/14/25
# Description: The urls file for the restaurant website. 

## restaurant/urls.py
## url patterns for the 'restaurant' app.

from django.urls import path
from django.conf import settings
from . import views 

# URL patterns for this app:
urlpatterns = [
    path(r'', views.main, name='main'), ## NEW
    path(r'main', views.main, name='main'), ## NEW
    path(r'order', views.order, name='order'), ## NEW
    path(r'confirmation', views.confirmation, name='confirmation'), ## NEW
]