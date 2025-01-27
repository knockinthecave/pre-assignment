from django.urls import path
from .views import (UserSignUpAPIView,
                    UserLoginAPIView,
                    UserTokenRefreshAPIView,
                    UserLogoutAPIView)

urlpatterns = [
    path('signup', UserSignUpAPIView.as_view(), name='signup'),
    path('login', UserLoginAPIView.as_view(), name='login'),
    path('refresh', UserTokenRefreshAPIView.as_view(), name='refresh'),
    path('logout', UserLogoutAPIView.as_view(), name='logout'),
]
