from django.urls import path
from . import views

urlpatterns = [
    path('', views.appointment_list, name='appointment-list'),
    path('book/', views.book_appointment, name='book-appointment'),
    path('<int:appointment_id>/status/<str:status>/', views.appointment_status_update, name='appointment-status-update'),
]
