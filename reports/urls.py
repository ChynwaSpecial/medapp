from django.urls import path
from . import views

urlpatterns = [
    path('patient/', views.patient_reports, name='patient-reports'),
    path('doctor/', views.doctor_reports, name='doctor-reports'),
    path('all/', views.all_reports, name='all-reports'),
    path('upload/', views.report_upload, name='report-upload'),
    path('download/<int:report_id>/', views.download_report, name='download-report'),
]
