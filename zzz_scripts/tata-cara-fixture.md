## CARA BIKIN FIXTURE

1. Copy JSON file `rumah_makan_data.json` dan `makanan_data.json` ke folder `/<app_name>/fixtures`

2. Replace `"yourapp"` di setiap model dengan nama app kalian
   Buat replace, bisa coba pencet CTRL + H di VSCode, ntar muncul buat replace

3. Copy ini ke `apps.py` di app kalian

-   Ganti `MainConfig` dengan nama config app kalian
-   Ganti `main` dengan nama app kalian

```python
from django.apps import AppConfig
from django.db.models.signals import post_migrate
from django.core.management import call_command


def load_fixtures(sender, **kwargs):
    # Debug
    print("========================\nLoading fixtures\n========================")
    try:
        call_command("loaddata", "rumah_makan_data.json")
        call_command("loaddata", "makanan_data.json")
    except Exception as e:
        print(f"Error loading fixtures: {e}")


# Example: If your app name is 'rating_toko', then replace 'MainConfig' with 'RatingTokoConfig'
# Don't forget to replace 'main' with your app name
class MainConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "main"

    def ready(self):
        post_migrate.connect(load_fixtures, sender=self)
```

4. Copy ini ke `__init__.py` di app kalian

-   Ganti `main` dengan nama app kalian

```python
default_app_config = 'main.apps.MainConfig'
```

5. Jangan lupa run `python manage.py makemigrations` dan `python manage.py migrate`, karena fixture itu kepanggil pas migrate database
