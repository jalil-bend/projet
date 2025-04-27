from django.db.models.signals import post_save
from django.dispatch import receiver
from users.models import Profile
from .models import Doctor

@receiver(post_save, sender=Profile)
def create_doctor(sender, instance, created, **kwargs):
    """ Crée automatiquement un objet Doctor si le profil est un ophtalmologue et est approuvé """
    if instance.speciality == "ophtalmologue" and instance.is_approved:
        Doctor.objects.get_or_create(profile=instance)

