# Generated by Django 5.1.2 on 2024-10-26 19:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('poll', '0004_alter_choice_choice_text'),
    ]

    operations = [
        migrations.AlterField(
            model_name='choice',
            name='choice_text',
            field=models.CharField(max_length=200),
        ),
    ]