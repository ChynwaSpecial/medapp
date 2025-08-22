from django.urls import path
from . import views

urlpatterns = [
    path('patient/', views.patient_billing, name='patient-billing'),
    path('doctor/', views.doctor_billing, name='doctor-billing'),
    path('admin/', views.admin_billing, name='admin-billing'),
    path('create/', views.create_invoice, name='create-invoice'),
    path('mark-paid/<int:invoice_id>/', views.mark_invoice_paid, name='mark-invoice-paid'),
]
