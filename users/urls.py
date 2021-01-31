"""Defines url patterns for users."""

from django.conf.urls import url
# from django.contrib.auth.views import login   #  ---> don't work
# from django.contrib.auth import authenticate, login
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # Login page.
    # url(r'^login/$', login, {'template_name': 'users/login.html'}, name='login'),
    # url(r'^login$', LoginView.as_view(), name='login'),
    # url('accounts/login/', auth_views.LoginView.as_view()),

    # Registration page
    url(r'^register/$', views.register, name='register'),

    ]