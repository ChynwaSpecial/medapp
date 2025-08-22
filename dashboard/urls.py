from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard_home, name='dashboard'),
    path('admin/', views.admin_dashboard, name='admin-dashboard'),
    path('doctor/', views.doctor_dashboard, name='doctor-dashboard'),
    path('patient/', views.patient_dashboard, name='patient-dashboard'),
    path('staff/', views.staff_dashboard, name='staff-dashboard'),
]
