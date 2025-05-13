from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Message



@receiver(post_save, sender=Message)
def update_conversation_last_updated(sender, instance, **kwargs):
    conversation = instance.conversation
    conversation.last_updated = instance.timestamp
    conversation.save(update_fields=['last_updated'])

from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.dispatch import receiver
from users.models import Profile

@receiver(user_logged_in)
def mark_user_online(sender, request, user, **kwargs):
    user.profile.is_online = True
    user.profile.save()

@receiver(user_logged_out)
def mark_user_offline(sender, request, user, **kwargs):
    user.profile.is_online = False
    user.profile.save()


from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.dispatch import receiver
from django.utils.timezone import now

@receiver(user_logged_in)
def set_user_online(sender, request, user, **kwargs):
    print("Signal reçu : user connecté")
    user.profile.is_online = True
    user.profile.last_seen = now()
    user.profile.save()


@receiver(user_logged_out)
def set_user_offline(sender, request, user, **kwargs):
    user.profile.is_online = False
    user.profile.last_seen = now()
    user.profile.save()

