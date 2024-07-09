from django.apps import AppConfig


class DiagramsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'diagrams'

    def ready(self):
        import diagrams.signals
        