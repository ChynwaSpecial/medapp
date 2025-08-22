from django.db import models
from django.conf import settings

class DoctorProfile(models.Model):
    SPECIALTY_CHOICES = [
        ('cardiology', 'Cardiology'),
        ('dermatology', 'Dermatology'),
        ('neurology', 'Neurology'),
        ('pediatrics', 'Pediatrics'),
        ('general', 'General Practice'),
        # Add more specialties as needed
    ]

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='doctor_profile')
    specialization = models.CharField(max_length=100, choices=SPECIALTY_CHOICES)
    bio = models.TextField(blank=True)
    phone = models.CharField(max_length=20, blank=True)
    office_address = models.TextField(blank=True)
    license_number = models.CharField(max_length=50, blank=True)
    experience_years = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"Dr. {self.user.get_full_name()} - {self.specialty}"
