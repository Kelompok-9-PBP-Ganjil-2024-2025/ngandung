from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.exceptions import ValidationError

class User(AbstractUser):
    ROLE_CHOICES = (
        ('user', 'User'),
        ('admin', 'Admin'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='user')

    def save(self, *args, **kwargs):
        if self.username == 'admin' and not self.pk:
            if User.objects.filter(username='admin').exists():
                raise ValidationError("Akun admin sudah ada.")
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        if self.username == 'admin':
            raise ValidationError("Tidak dapat menghapus akun admin.")
        super().delete(*args, **kwargs)
