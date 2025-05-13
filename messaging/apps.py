from django.apps import AppConfig


class MessagingConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'messaging'

def ready(self):
    print("✅ messaging.apps.MessagingConfig loaded")
    import messaging.signals

