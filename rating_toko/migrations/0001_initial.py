# Generated by Django 5.1.1 on 2024-10-25 09:25

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='RumahMakan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('kode_provinsi', models.IntegerField()),
                ('nama_provinsi', models.CharField(max_length=100)),
                ('bps_kode_kabupaten_kota', models.IntegerField()),
                ('bps_nama_kabupaten_kota', models.CharField(max_length=100)),
                ('nama_rumah_makan', models.CharField(max_length=100)),
                ('alamat', models.CharField(max_length=255)),
                ('latitude', models.DecimalField(decimal_places=6, max_digits=9)),
                ('longitude', models.DecimalField(decimal_places=6, max_digits=9)),
                ('tahun', models.IntegerField()),
                ('masakan_dari_mana', models.CharField(max_length=50)),
                ('makanan_berat_ringan', models.CharField(max_length=50)),
            ],
        ),
    ]