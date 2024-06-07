from django.apps import AppConfig
from django.db.models.signals import post_migrate


class ApiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'api'

    def ready(self):
        post_migrate.connect(populate_sample_data, sender=self)


def populate_sample_data(sender, **kwargs):
    from .sample_data import create_sample_data
    create_sample_data()
