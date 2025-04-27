from django.contrib import admin
from .models import User, Profile
from django.contrib.auth.admin import UserAdmin
from django.conf import settings
from django.core.mail import send_mail

class CustomUserAdmin(UserAdmin):
    list_display = (
        'username', 
        'email', 
        'first_name', 
        'last_name', 
        'is_active',
        'get_is_approved',
        'get_card_verified',
    )

    def get_is_approved(self, obj):
        return obj.profile.is_approved if hasattr(obj, 'profile') else False
    get_is_approved.boolean = True
    get_is_approved.short_description = 'Approuvé'

    def get_card_verified(self, obj):
        return obj.profile.card_verified if hasattr(obj, 'profile') else False
    get_card_verified.boolean = True
    get_card_verified.short_description = 'Carte vérifiée'

    list_filter = ('is_active', 'profile__speciality', 'profile__card_verified',)
    search_fields = ('username', 'email', 'first_name', 'last_name')
    ordering = ('username',)
    fieldsets = (
        (None, {'fields': ('username', 'password')}), 
        ('Informations personnelles', {'fields': ('first_name', 'last_name', 'email')}),
        ('Permissions', {'fields': ('is_active',)}),
        ('Dates importantes', {'fields': ('last_login', 'date_joined')}),
    )

    def save_model(self, request, obj, form, change):
        if not obj.is_superuser:
            obj.is_staff = False
            obj.is_superuser = False
        if hasattr(obj, 'profile') and obj.profile.is_approved and obj.is_active:
            obj.is_active = True
        super().save_model(request, obj, form, change)


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'speciality', 'card_verified')
    list_filter = ('speciality', 'card_verified')
    search_fields = ('user__username', 'user__email', 'user__first_name', 'user__last_name')

    def save_model(self, request, obj, form, change):
        # On envoie un mail et on gère Doctor à CHAQUE sauvegarde d'un profil ophtalmologue
        super().save_model(request, obj, form, change)
        if obj.speciality == 'ophtalmologue' and obj.is_approved:
            from docteur.models import Doctor
            # Crée ou met à jour le Doctor lié à ce profil
            Doctor.objects.update_or_create(
                profile=obj,
                defaults={
                    'specialization': getattr(obj, 'speciality', 'Généraliste'),
                    'experience_years': 0,  # Adapte si tu veux
                }
            )
            # Envoi du mail
            from django.core.mail import send_mail
            from django.conf import settings
            title = "Dr."
            send_mail(
                subject="Votre compte est validé !",
                message=f"Bonjour {title} {obj.user.first_name},\n\nVotre compte est validé ou mis à jour par l'administrateur. Vous pouvez accéder à la plateforme.\n\nCordialement,\nL'équipe OPTO DZ",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[obj.user.email],
                fail_silently=False,
            )

    def approve_users(self, request, queryset):
        for profile in queryset:
            profile.is_approved = True
            profile.save()
            # Créer un docteur seulement si c'est un ophtalmologue et qu'il n'existe pas déjà
            if profile.user_type == 'ophtalmologue' and not hasattr(profile, 'doctor_profile'):
                Doctor.objects.create(profile=profile, specialization="Généraliste", experience_years=0)
        self.message_user(request, "Les utilisateurs sélectionnés ont été approuvés et ajoutés en tant que docteurs.")


admin.site.register(User, CustomUserAdmin)
admin.site.register(Profile, ProfileAdmin)
