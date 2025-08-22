from django.urls import path
from .views import custom_login
from django.contrib.auth.views import LogoutView
from . import views
from dashboard.views import patient_dashboard
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('login/', custom_login, name='login'),
    path('accounts/password-reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('accounts/password-reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('accounts/reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('accounts/reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('register/', views.register, name='register'),
    path('patient/dashboard/', patient_dashboard, name='patient-dashboard'),
    path('doctors/', views.doctor_list, name='doctor-list'),
    path('patients/', views.patient_list, name='patient-list'),
]
