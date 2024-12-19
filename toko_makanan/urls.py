from django.urls import path
from toko_makanan.views import *

app_name = 'toko_makanan'

urlpatterns = [
    path("", show_main, name="show_main"),
    path('add-toko/', create_toko, name='add_toko'),
    path('edit-toko/<int:id>/', edit_toko, name='edit_toko'),
    path('delete-toko/<int:id>/', delete_toko, name='delete_toko'),
    path('add-makanan/', add_makanan_ajax, name='add_makanan'),
    path('edit-makanan/<int:id>/', edit_makanan, name='edit_makanan'),
    path('detail-rumah-makan/<int:id>/', detail_rumah_makan, name='detail_rumah_makan'),
    path('delete-makanan/<int:id>/', delete_makanan, name='delete_makanan'),
    path('makanan-json/', makanan_json, name='makanan_json'),
    path('detail-json/<int:id>/', rumahmakan_detail_json, name='rumahmakan_detail_json'),
]