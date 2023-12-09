from django.apps import AppConfig


class AppCreditosConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app_creditos'

    def ready(self):
        import app_creditos.signals