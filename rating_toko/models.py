from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User


class RumahMakan(models.Model):
    kode_provinsi = models.IntegerField()
    nama_provinsi = models.CharField(max_length=100)
    bps_kode_kabupaten_kota = models.IntegerField()
    bps_nama_kabupaten_kota = models.CharField(max_length=100)
    nama_rumah_makan = models.CharField(max_length=150)
    alamat = models.CharField(max_length=255)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    tahun = models.IntegerField()
    masakan_dari_mana = models.CharField(max_length=50)
    makanan_berat_ringan = models.CharField(max_length=50)
    average_rating = models.DecimalField(max_digits=2, decimal_places=1, default=0.0)
    number_of_ratings = models.IntegerField(default=0)

    def __str__(self):
        return self.nama_rumah_makan


class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rumah_makan = models.ForeignKey(RumahMakan, on_delete=models.CASCADE)
    rating = models.IntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(5),
        ]
    )
    review = models.TextField()
    tanggal = models.DateField(auto_now_add=True)
