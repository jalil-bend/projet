from django.db import models
from django.conf import settings
from docteur.models import Doctor
import os 
import random
import string

class Patient(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)  # Compte patient
    doctors = models.ManyToManyField(Doctor, related_name="patients")  # Relation plusieurs médecins - plusieurs patients
    
    # Informations générales
    first_name = models.CharField(max_length=50, verbose_name="Nom")
    last_name = models.CharField(max_length=50, verbose_name="Prénom")
    birth_date = models.DateField(verbose_name="Date de naissance")
    profession = models.CharField(max_length=100, blank=True, null=True, verbose_name="Profession")
    email = models.EmailField(unique=True, blank=True, null=True)
    phone = models.CharField(max_length=15, verbose_name="Numéro de téléphone") 
    birth_place = models.CharField(max_length=100, verbose_name="Lieu de naissance")

    # Dossier médical
    remarks = models.CharField(blank=True, null=True, verbose_name="Remarques", max_length=300)  # Remarques du médecin
    diagnosis = models.CharField(blank=True, null=True, verbose_name="Diagnostic", max_length=300)  # Diagnostic
    prescription = models.CharField(blank=True, null=True, verbose_name="Traitement", max_length=300)  # Traitement

    # Correction visuelle (tableau de valeurs)
    sphere_right_vl = models.FloatField(blank=True, null=True, verbose_name="Sphère OD VL")
    cylinder_right_vl = models.FloatField(blank=True, null=True, verbose_name="Cylindre OD VL")
    axis_right_vl = models.IntegerField(blank=True, null=True, verbose_name="Axe OD VL ")
    sphere_left_vl = models.FloatField(blank=True, null=True, verbose_name="Sphère OG VL")
    cylinder_left_vl = models.FloatField(blank=True, null=True, verbose_name="Cylindre OG VL")
    axis_left_vl = models.IntegerField(blank=True, null=True, verbose_name="Axe OG VL")


    sphere_right_vp = models.FloatField(blank=True, null=True, verbose_name="Sphère OD VP")
    cylinder_right_vp = models.FloatField(blank=True, null=True, verbose_name="Cylindre OD VP")
    axis_right_vp = models.IntegerField(blank=True, null=True, verbose_name="Axe OD VP")
    sphere_left_vp = models.FloatField(blank=True, null=True, verbose_name="Sphère OG VP")
    cylinder_left_vp = models.FloatField(blank=True, null=True, verbose_name="Cylindre OG VP")
    axis_left_vp = models.IntegerField(blank=True, null=True, verbose_name="Axe OG VP")

    

    # Gestion des consultations
    consultation_date = models.DateTimeField(auto_now_add=True, verbose_name="Date de consultation")  # Date automatique de la visite
    next_appointment = models.DateTimeField(blank=True, null=True, verbose_name="Prochain rendez-vous")  # Prochain rendez-vous

    has_account = models.BooleanField(default=False)  # Par défaut, pas de compte
    access_password = models.CharField(max_length=12, blank=True, null=True)  # Mot de passe secondaire pour accès
    
    class Meta:
        unique_together = ('first_name', 'last_name', 'birth_date')  # 🔹 Empêche les doublons

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.email if self.email else 'Sans compte'}"

    # 🔹 Générer un identifiant unique
    def generate_username(self):
        return f"{self.first_name.lower()}{random.randint(100, 999)}"

    # 🔹 Générer un mot de passe
    def generate_password(self):
        return ''.join(random.choices(string.ascii_letters + string.digits, k=8))

    # 🔹 Création automatique du compte patient
    def create_user_account(self, email):
        if not self.user and email:  # Si le patient n'a pas encore de compte
            username = self.generate_username()
            password = self.generate_password()
            access_password = self.generate_password()  # Mot de passe secondaire

            user = User.objects.create_user(
                username=username,
                password=password,
                email=email,
                first_name=self.first_name,
                last_name=self.last_name
            )
            self.user = user
            self.has_account = True
            self.access_password = access_password
            self.email = email
            self.save()
            return username, password, access_password  # Retourne les identifiants générés
        return None

        # 🔹 Vérification avant d'enregistrer (évite les doublons)
    def save(self, *args, **kwargs):
     if Patient.objects.filter(
        first_name=self.first_name, 
        last_name=self.last_name, 
        birth_date=self.birth_date
     ).exclude(pk=self.pk).exists():
        raise ValueError("Un patient avec ce nom et cette date de naissance existe déjà.")
    
     super().save(*args, **kwargs)




def medical_image_path(instance, filename):
    """Définit le chemin de stockage en fonction du type d'image."""
    folder = instance.image_type.replace(" ", "_")  # Remplace les espaces par des underscores
    return f'medical_images/{folder}/{filename}'

# class MedicalImage(models.Model):
#     IMAGE_TYPES = [
#         ('OCT', 'OCT'),
#         ('Scanner', 'Scanner'),
#         ('Topographie', 'Topographie'),
#         ('IRM', 'IRM'),
#     ]

#     patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name="medical_images")
#     image = models.ImageField(upload_to=medical_image_path)
#     image_type = models.CharField(max_length=20, choices=IMAGE_TYPES)

#     def __str__(self):
#         return f"{self.patient.first_name} {self.patient.last_name} - {self.image_type}"


class FicheClinique(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='fiches_cliniques')
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    date_modification = models.DateTimeField(auto_now_add=True)

    antecedents = models.TextField(blank=True, null=True)
    diagnostic = models.TextField(blank=True, null=True)
    traitement = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ['-date_modification']

    def __str__(self):
        return f"Fiche du {self.date_modification.strftime('%d/%m/%Y')} - {self.doctor}"


class RendezVous(models.Model):
    STATUS_CHOICES = [
        ('Confirmé', 'Confirmé'),
        ('En attente', 'En attente'),
        ('Annulé', 'Annulé'),
    ]

    ORIGINE_CHOICES = [
        ('Manuel', 'Ajout manuel'),
        ('Dossier médical', 'Créé depuis un dossier médical'),
        ('Autre', 'Autre origine')
    ]

    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name="rendez_vous")
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name="rendez_vous")
    date = models.DateTimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='En attente')
    origine = models.CharField(max_length=50, choices=ORIGINE_CHOICES, default='Manuel',  verbose_name="Origine du rendez-vous")
    description = models.TextField(blank=True, null=True)
    est_confirme = models.BooleanField(default=False)
    class Meta:
        ordering = ['-date']

    def __str__(self):
        return f"{self.patient.first_name} {self.patient.last_name} - {self.date.strftime('%d/%m/%Y %H:%M')} - {self.status}"







# Create your models here.
