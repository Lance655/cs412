# File: urls.py
# Author: Lance Sinson (ssinson@bu.edu), 3/28/25
# Description: The urls file for the mini_fb website. 

from django.urls import path
from .views import * # ShowAllProfilesView, ShowProfilePageView, CreateProfileView, CreateStatusMessageView, UpdateProfileView

# generic view for authentication/authorization
from django.contrib.auth import views as auth_views # NEW

urlpatterns = [
    path('', ShowAllProfilesView.as_view(), name="show_all_profiles"),
    path('profile/<int:pk>', ShowProfilePageView.as_view(), name="show_profile"),
    path('create_profile', CreateProfileView.as_view(), name="create_profile" ),
    path('profile/create_status', CreateStatusMessageView.as_view(), name="create_status"),                         # removed int pk
    path('profile/update', UpdateProfileView.as_view(), name="update_profile"),                                     # removed int pk
    path('status/<int:pk>/delete', DeleteStatusMessageView.as_view(), name="delete_status"),
    path('status/<int:pk>/update', UpdateStatusMessageView.as_view(), name="update_status"),            
    path('profile/add_friend/<int:other_pk>', CreateFriendView.as_view(), name="create_friend"),                    # removed int pk
    path('profile/friend_suggestions', ShowFriendSuggestionsView.as_view(), name="show_friend_suggestions"),        # removed int pk
    path('profile/news_feed', ShowNewsFeedView.as_view(), name="news_feed"),                                        # removed int pk
    path('login/', auth_views.LoginView.as_view(template_name='mini_fb/login.html'), name="login"),
    path('logout/', auth_views.LogoutView.as_view(template_name='mini_fb/logged_out.html'), name="logout"),
]
