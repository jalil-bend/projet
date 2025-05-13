from django.db import models
from django.conf import settings

class Doctor(models.Model):
    profile = models.OneToOneField('users.Profile', on_delete=models.CASCADE, related_name="doctor_profile")


    WORKPLACE_CHOICES = [
        ('privé', 'Privé'),
        ('hopital', 'Hopital'),
        ('clinique', 'Clinique'),
    ]    

    def doctor_photo_path(instance, filename):
    # Sauvegarde la photo dans media/profile_pics/
     return f'profile_pics/doctor_{instance.id}/{filename}'
     
    # Informations professionnelles
    photo = models.ImageField(
    upload_to=doctor_photo_path,  
    blank=True, 
    null=True, 
    default='doc_profile_pics/photo_defaut.jpg',  
    verbose_name="Photo de profil"
)



    workplace_type = models.CharField(blank=True, null=True, max_length=20, choices=WORKPLACE_CHOICES, verbose_name="Type de lieu de travail")
    workplace_name = models.CharField(blank=True, null=True, max_length=255, verbose_name="Nom du lieu de travail")
    experience_years = models.IntegerField(default=0, verbose_name="Années d'expérience")
    specialization = models.CharField(max_length=255, blank=True, null=True, verbose_name="Spécialisation détaillée")
    bio = models.TextField(blank=True, null=True, verbose_name="Biographie")

    # Coordonnées
    phone_number = models.CharField(max_length=10, blank=True, null=True, verbose_name="Numéro de téléphone")
    address = models.TextField(blank=True, null=True, verbose_name="Adresse")
    city = models.CharField(max_length=100, blank=True, null=True, verbose_name="Ville")
    

    # Informations supplémentaires
    consultation_fee = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, verbose_name="Frais de consultation")
    availability_dim = models.TextField(blank=True, null=True, verbose_name="Disponibilité dimanche")
    availability_lun = models.TextField(blank=True, null=True, verbose_name="Disponibilité lundi")
    availability_mar = models.TextField(blank=True, null=True, verbose_name="Disponibilité mardi")
    availability_mer = models.TextField(blank=True, null=True, verbose_name="Disponibilité mercredi")
    availability_jeu = models.TextField(blank=True, null=True, verbose_name="Disponibilité jeudi")
    availability_ven = models.TextField(blank=True, null=True, verbose_name="Disponibilité vendredi")
    availability_sam = models.TextField(blank=True, null=True, verbose_name="Disponibilité samedi")
    website = models.URLField(blank=True, null=True, verbose_name="Site web")
    social_media = models.JSONField(blank=True, null=True, verbose_name="Réseaux sociaux (JSON)")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Dr. {self.profile.user.first_name} {self.profile.user.last_name} - {self.specialization or self.profile.speciality or 'Ophtalmologue'}" 

    def get_photo_url(self):
     if self.photo and self.photo.name != 'doc_profile_pics/photo_defaut.jpg':
        return self.photo.url
     return settings.MEDIA_URL + 'doc_profile_pics/photo_defaut.jpg'
