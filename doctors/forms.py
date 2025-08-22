from django import forms
from .models import DoctorProfile

class DoctorProfileForm(forms.ModelForm):
    class Meta:
        model = DoctorProfile
        fields = [
            'specialization',
            'bio',
            'phone',
            'office_address',
            'license_number',
            'experience_years'
        ]
