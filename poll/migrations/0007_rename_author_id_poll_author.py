# Generated by Django 5.1.4 on 2024-12-16 09:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('poll', '0006_rename_author_poll_author_id'),
    ]

    operations = [
        migrations.RenameField(
            model_name='poll',
            old_name='author_id',
            new_name='author',
        ),
    ]
