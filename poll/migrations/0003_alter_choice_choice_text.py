# Generated by Django 5.1.2 on 2024-10-26 19:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('poll', '0002_alter_choice_choice_text'),
    ]

    operations = [
        migrations.AlterField(
            model_name='choice',
            name='choice_text',
            field=models.CharField(max_length=200),
        ),
    ]