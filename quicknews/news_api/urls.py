from django.urls import path
from . import views
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.contrib.auth import views as auth_views


def custom_logout_view(request):
    logout(request)  # Log the user out
    return redirect('login')  # Redirect to login page

urlpatterns = [
    path('', views.home, name='home'),
    path('accounts/login/', auth_views.LoginView.as_view(), name='login'),
    path('accounts/logout/', custom_logout_view, name='logout'),
    path('accounts/register/', views.register, name='register'),  # Register path if applicable
    path('update_notes/', views.update_notes, name='update_notes'),
]
