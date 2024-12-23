from django.db import models
from django.contrib.auth.models import User
from main.models import RumahMakan
from django.contrib.auth.models import AbstractUser
    
class UserProfile(models.Model): #Ini juga
    favorit_toko = models.ManyToManyField(RumahMakan, related_name='pengguna_favorit')
    

    def __str__(self):
        return self.user.username
    
    def tambah_favorit(self, RumahMakan):
        self.favorit_toko.add(RumahMakan)
        self.save()

class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rumah_makan = models.ForeignKey(RumahMakan, on_delete=models.CASCADE)
    
    
