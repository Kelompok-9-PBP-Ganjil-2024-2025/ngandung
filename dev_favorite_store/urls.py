from django.urls import path
from .views import *

app_name = 'dev_favorite_store'

urlpatterns = [
    path('tambah-ke-favorit/<int:rumah_makan_id>', tambah_ke_favorite, name='tambah_ke_favorit'),
    path('hapus-dari-favorit/<int:toko_id>/', hapus_dari_favorit, name='hapus_dari_favorit'),
    path('daftar-favorit/', daftar_favorit, name='daftar_favorit'),
    path('api/user/favorites/', user_favorite_restaurants, name='user-favorites'),
    path('api/user/favorites/add/<int:rumah_makan_id>/', add_to_favorite, name='add_to_favorite'),
    path('api/user/favorites/<int:favorite_id>/delete/', delete_favorite, name='delete_favorite'),
]