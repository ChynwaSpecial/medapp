from django import forms
from .models import PatientProfile

class PatientProfileForm(forms.ModelForm):
    class Meta:
        model = PatientProfile
        fields = ['date_of_birth', 'gender', 'phone', 'address', 'blood_group', 'allergies', 'medical_history']
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'gender': forms.Select(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'placeholder': 'e.g. +234...', 'class': 'form-control'}),
            'address': forms.Textarea(attrs={'rows': 2, 'class': 'form-control'}),
            'blood_group': forms.Select(attrs={'class': 'form-control'}),
            'allergies': forms.Textarea(attrs={'rows': 2, 'class': 'form-control'}),
            'medical_history': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
        }
        labels = {
            'date_of_birth': 'Date of Birth',
            'phone': 'Phone Number',
            'medical_history': 'Medical History Summary',
        }
