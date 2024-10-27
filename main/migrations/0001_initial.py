

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Toko',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nama', models.CharField(max_length=100)),
                ('alamat', models.CharField(max_length=255)),
                ('telpon', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Makanan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nama', models.CharField(max_length=100)),
                ('harga', models.DecimalField(decimal_places=2, max_digits=8)),
                ('description', models.TextField(blank=True, null=True)),
                ('toko', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.toko')),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('favorit_toko', models.ManyToManyField(related_name='pengguna_favorit', to='main.toko')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
