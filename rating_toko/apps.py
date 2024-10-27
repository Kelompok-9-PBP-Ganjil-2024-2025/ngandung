from django.apps import AppConfig
from django.db.models.signals import post_migrate
from django.core.management import call_command


def load_fixtures(sender, **kwargs):
    # Debug
    print("========================\nLoading fixtures\n========================")
    try:
        call_command("loaddata", "rumah_makan_data.json")
    except Exception as e:
        print(f"Error loading fixtures: {e}")


class RatingTokoConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "rating_toko"

    def ready(self):
        post_migrate.connect(load_fixtures, sender=self)