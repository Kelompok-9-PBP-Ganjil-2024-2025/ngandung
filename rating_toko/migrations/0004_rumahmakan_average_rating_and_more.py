# Generated by Django 5.1.1 on 2024-10-26 10:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rating_toko', '0003_rating'),
    ]

    operations = [
        migrations.AddField(
            model_name='rumahmakan',
            name='average_rating',
            field=models.DecimalField(decimal_places=1, default=0.0, max_digits=2),
        ),
        migrations.AddField(
            model_name='rumahmakan',
            name='number_of_ratings',
            field=models.IntegerField(default=0),
        ),
    ]