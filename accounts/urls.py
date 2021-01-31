"""Defines url patterns for users."""

from django.conf.urls import url
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # Login page.
    url('accounts/login/',
        auth_views.LoginView.as_view(template_name='accounts/login.html')),
    # Logout page
    url(r'^logout/$', auth_views.LogoutView.as_view(template_name='accounts/logout.html')),


    ]