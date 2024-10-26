from django.db import models
from django.contrib.auth.models import User
from main.models import RumahMakan

# class Toko(models.Model):
#     nama = models.CharField(max_length=100)
#     alamat = models.CharField(max_length=255)
#     telpon = models.CharField(max_length=20)

#     def __str__(self) -> str:
#         return self.nama
    
# class Makanan(models.Model): #Nanti class ini diapus, baru import class dari folder tambah makanan
#     nama = models.CharField(max_length=100)
#     harga = models.DecimalField(max_digits=8, decimal_places=2)
#     toko = models.ForeignKey(Toko, on_delete=models.CASCADE)
#     description = models.TextField(null=True, blank=True)

#     def __str__(self):
#         return self.nama
    
class UserProfile(models.Model): #Ini juga
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    favorit_toko = models.ManyToManyField(RumahMakan, related_name='pengguna_favorit')

    def __str__(self):
        return self.user.username
    
    def tambah_favorit(self, RumahMakan):
        self.favorit_toko.add(RumahMakan)
        self.save()
