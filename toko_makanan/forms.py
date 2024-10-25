from django.forms import ModelForm
from toko_makanan.models import RumahMakan, Makanan

class FormRumahMakan(ModelForm):
    class Meta:
        model = RumahMakan
        fields = [
            'kode_provinsi', 
            'nama_provinsi', 
            'bps_kode_kabupaten_kota', 
            'bps_nama_kabupaten_kota',  
            'nama_rumah_makan',
            'alamat',
            'latitude',
            'longitude',
            'tahun',
            'masakan_dari_mana',
            'makanan_berat_ringan',
            ]

class FormMakanan(ModelForm):
    class Meta:
        model = Makanan
        fields = ['name', 'price', 'rumah_makan']