from django.urls import path
from . import views

urlpatterns = [
    path('profile/', views.profile_view, name='doctor-profile'),
    path('profile/edit/', views.profile_edit, name='doctor-profile-edit'),
]
