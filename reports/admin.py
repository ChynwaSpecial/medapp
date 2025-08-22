from django.contrib import admin
from .models import MedicalReport

@admin.register(MedicalReport)
class MedicalReportAdmin(admin.ModelAdmin):
    list_display = ('title', 'patient', 'doctor', 'created_at')
    search_fields = ('title', 'patient__email', 'doctor__email')
    list_filter = ('created_at',)
