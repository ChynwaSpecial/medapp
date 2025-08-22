from django.contrib import admin
from .models import DoctorProfile

@admin.register(DoctorProfile)
class DoctorProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'specialization', 'experience_years', 'phone')
    search_fields = ('user__email', 'user__first_name', 'user__last_name', 'specialization')
