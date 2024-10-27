from django.db import models


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

    def __str__(self):
        return self.nama_rumah_makan


class Makanan(models.Model):
    name = models.CharField(max_length=100)
    price = models.IntegerField()
    rumah_makan = models.ForeignKey(
        # If a RumahMakan is deleted, all of its related Makanan will be deleted as well
        RumahMakan,
        on_delete=models.CASCADE,
        related_name="makanan",
    )

    def __str__(self):
        return f"{self.name} - {self.price}"
