from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.core.mail import send_mail
#from docteur.models import Doctor

class User(AbstractUser):
    ROLE_CHOICES = (
        ('ophtalmologue', 'Ophtalmologue'),
        ('optometriste', 'Optometriste'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    def save(self, *args, **kwargs):
       if not self.is_superuser:
           self.is_staff = False
           self.is_superuser = False
           super().save(*args, **kwargs)

class Profile(models.Model):
    SPECIALITY_CHOICES = [
        ('ophtalmologue', 'Ophtalmologue'),
        ('optometriste', 'Optometriste'),
    ]
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')
    speciality = models.CharField(max_length=20, choices=SPECIALITY_CHOICES)
    is_approved = models.BooleanField(default=False)
    card_verified = models.BooleanField(default=False)
    last_seen = models.DateTimeField(null=True, blank=True)
    is_typing = models.BooleanField(default=False)
    last_typing = models.DateTimeField(null=True, blank=True)
    is_online = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        was_approved = self.is_approved  

        if self.card_verified:
            self.is_approved = True

        super().save(*args, **kwargs)

        print(f"DEBUG: Profile sauvegardé pour {self.user.username}, is_approved={self.is_approved}, speciality={self.speciality}")

        if not was_approved and self.is_approved and self.speciality == "ophtalmologue":
            from docteur.models import Doctor  # IMPORT LOCAL pour éviter l'import circulaire
            doctor, created = Doctor.objects.get_or_create(profile=self, defaults={
                'specialization': self.speciality,
                'experience_years': 0, 
            })
            print(f"DEBUG: Doctor créé ? {created} pour {self.user.username}")

        if not was_approved and self.is_approved:
            title = "Dr" if self.speciality == "ophtalmologue" else "Mr"
            print(f"DEBUG: Envoi de l'email à {self.user.email}")
            send_mail(
                subject="Votre compte est approuvé !",
                message=f"Bonjour {title} {self.user.first_name},\n\nVotre compte a été approuvé. Vous pouvez maintenant accéder à toutes les fonctionnalités de la plateforme.\n\n Nous vous remercions énormément pour votre confiance et pour votre coopération.\n\n Cordialement,\nL'équipe OPTO DZ",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[self.user.email],
                fail_silently=False,
            )
            print("DEBUG: Email envoyé avec succès")

    def __str__(self):
        return f"{self.user.username} - {self.speciality} - {'Approuvé' if self.is_approved else 'En attente'}"

    def get_photo_url(self):
        # Si ce profil appartient à un ophtalmologue, on retourne sa photo
        if hasattr(self, 'doctor_profile') and self.doctor_profile.photo:
            return self.doctor_profile.get_photo_url()
        # Sinon on retourne une photo par défaut
        return '/media/doc_profile_pics/photo_defaut.jpg'

# Create your models here.
