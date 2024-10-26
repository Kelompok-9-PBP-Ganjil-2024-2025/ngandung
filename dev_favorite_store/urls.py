from django.urls import path
from .views import *

app_name = 'dev_favorite_store'

urlpatterns = [
    path('', show_main, name='show_main'),
    path('tambah-ke-favorit/<int:toko_id>/', tambah_ke_favorit, name='tambah_ke_favorit'),
    path('hapus-dari-favorit/<int:toko_id>/', hapus_dari_favorit, name='hapus_dari_favorit'),
    path('daftar-favorit/', daftar_favorit, name='daftar_favorit'),
]