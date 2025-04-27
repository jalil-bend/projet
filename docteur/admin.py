from django.contrib import admin
from .models import Doctor


@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ('get_full_name', 'specialization', 'experience_years', 'city', 'workplace_type', 'workplace_name')
    search_fields = ('profile__user__first_name', 'profile__user__last_name', 'phone_number', 'profile__user__email', 'city', 'workplace_name')
    list_filter = ('city', 'specialization', 'workplace_type')

    fieldsets = (
        ("Informations Générales", {"fields": ("profile","photo", "specialization", "bio")}),
        ("Expérience", {"fields": ("experience_years",)}),
        ("Lieu de Travail", {"fields": ("workplace_type", "workplace_name")}),
        ("Contact", {"fields": ("phone_number", "city")}),
    )

    def get_full_name(self, obj):
        return f"{obj.profile.user.first_name} {obj.profile.user.last_name}"
    
    get_full_name.short_description = "Nom et Prénom"




# Register your models here.
