from django.db import models

# Create your models here.
class Toko(models.Model):
    nama = models.CharField(max_length=100)
    alamat = models.CharField(max_length=255)
    telpon = models.CharField(max_length=20)

    def __str__(self) -> str:
        return self.nama

class Makanan(models.Model):
    nama = models.CharField(max_length=100)
    harga = models.DecimalField(max_digits=8, decimal_places=2)
    toko = models.ForeignKey(Toko, on_delete=models.CASCADE)
    description = models.TextField(null=True, blank=True)

    def __str__(self) -> str:
        return self.nama