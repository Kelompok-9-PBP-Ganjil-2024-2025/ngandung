from django.forms import ModelForm
from toko_makanan.models import Toko, Makanan

class FormToko(ModelForm):
    class Meta:
        model = Toko
        fields = ['nama', 'alamat', 'telpon']

class FormMakanan(ModelForm):
    class Meta:
        model = Makanan
        fields = ['nama', 'harga', 'toko']