from django.apps import AppConfig


class DevAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'dev_app'

    def ready(self):
        import dev_app.signals
