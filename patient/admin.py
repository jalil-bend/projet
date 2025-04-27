from django.contrib import admin
from .models import Patient


@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'phone', 'consultation_date', 'next_appointment')
    search_fields = ('first_name', 'last_name', 'email')
    list_filter = ('consultation_date', 'next_appointment')



# Register your models here.
