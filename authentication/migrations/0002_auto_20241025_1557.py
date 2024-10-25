# authentication/migrations/0002_create_admin.py
from django.db import migrations
from django.contrib.auth.hashers import make_password

def create_admin_user(apps, schema_editor):
    User = apps.get_model('authentication', 'User')
    if not User.objects.filter(username='admin').exists():
        User.objects.create(
            username='admin',
            password=make_password('1234hahahaha'),  # Ganti dengan password yang diinginkan
            role='admin',
            is_staff=True,
            is_superuser=True,
            email='admin@example.com',  # Ganti dengan email admin
        )

class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0001_initial'),  # Ganti dengan dependency yang benar
    ]

    operations = [
        migrations.RunPython(create_admin_user),
    ]
