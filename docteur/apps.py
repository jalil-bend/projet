from django.apps import AppConfig


class DocteurConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'docteur'


def ready(self):
        import docteur.signals