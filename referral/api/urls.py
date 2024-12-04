from django.urls import path

from .views import (
    ActivateInviteView,
    PhoneAuthView,
    ProfileView,
    UsersListView,
    VerifyView
)

urlpatterns = [
    path('auth/', PhoneAuthView.as_view(), name='api_auth'),
    path('verify/', VerifyView.as_view(), name='api_verify'),
    path('profile/', ProfileView.as_view(), name='api_profile'),
    path('users/', UsersListView.as_view(), name='users_list'),
    path(
        'activate-invite/',
        ActivateInviteView.as_view(),
        name='api_activate_invite'
    ),
]
