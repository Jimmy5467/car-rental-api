from django.contrib import admin
from django.urls import path, include
from .views import RegisterAPI,LoginAPI,ChangePasswordView, LogoutAllView, LogoutAPIView
from knox import views as knox_views
from rest_framework_simplejwt import views as jwt_views

urlpatterns = [
    path('register/', RegisterAPI.as_view(), name='register'),
    path('login/', jwt_views.TokenObtainPairView.as_view(), name='login'),
    path('login/refresh/', jwt_views.TokenRefreshView.as_view(), name='refresh'),
    path('logout/', LogoutAPIView.as_view(), name='logout'),
    path('logoutall/', LogoutAllView.as_view(), name='logoutall'),
    path('change-password/', ChangePasswordView.as_view(), name='change-password'),
    # path('api/password_reset/', include('django_rest_passwordreset.urls', namespace='password_reset')),
    # path('login/', LoginAPI.as_view(), name='login'),
    # path('logout/', knox_views.LogoutView.as_view(), name='logout'),
]
