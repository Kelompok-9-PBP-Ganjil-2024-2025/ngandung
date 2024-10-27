from django.db import models
from django.contrib.auth.models import User
from main.models import RumahMakan
    
class UserProfile(models.Model): #Ini juga
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    favorit_toko = models.ManyToManyField(RumahMakan, related_name='pengguna_favorit')

    def __str__(self):
        return self.user.username
    
    def tambah_favorit(self, RumahMakan):
        self.favorit_toko.add(RumahMakan)
        self.save()
