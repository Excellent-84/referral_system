from django.contrib.auth.views import LogoutView
from django.urls import path

from .views import auth_view, home, profile_view, verify_view

urlpatterns = [
    path('', home, name='home'),
    path('auth/', auth_view, name='auth'),
    path('verify/', verify_view, name='verify'),
    path('profile/', profile_view, name='profile'),
    path('logout/', LogoutView.as_view(), name='logout'),
]
