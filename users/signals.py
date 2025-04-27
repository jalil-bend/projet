from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from .models import User

@receiver(post_save, sender=User)
def user_status_changed(sender, instance, created, **kwargs):
    """ Envoie un email lorsque le compte est activé. """
    if not created:  # Vérifie que ce n'est pas une création de compte
        try:
            old_instance = User.objects.get(pk=instance.pk)
            if not old_instance.is_active and instance.is_active:
                subject = "Votre compte a été activé"
                message = (
                    f"Bonjour {instance.first_name},\n\n"
                    "Votre compte a été validé par l'administrateur. "
                    "Vous pouvez maintenant vous connecter à votre compte.\n\n"
                    "Cordialement,\nL'équipe OPTO DZ"
                )
                

                send_mail(
                    subject,
                    message,
                    settings.DEFAULT_FROM_EMAIL,
                    [instance.email],
                    fail_silently=False,
                )

            if instance.speciality == "ophtalmologue":
                Doctor.objects.get_or_create(profile=instance)
        except User.DoesNotExist:
            pass
