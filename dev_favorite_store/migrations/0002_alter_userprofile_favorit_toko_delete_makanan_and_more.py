# Generated by Django 5.1.2 on 2024-10-25 11:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dev_favorite_store', '0001_initial'),
        ('main', '0002_rumahmakan_remove_userprofile_favorit_toko_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='favorit_toko',
            field=models.ManyToManyField(related_name='pengguna_favorit', to='main.rumahmakan'),
        ),
        migrations.DeleteModel(
            name='Makanan',
        ),
        migrations.DeleteModel(
            name='Toko',
        ),
    ]
