from django.urls import path
from toko_makanan.views import *

app_name = 'toko_makanan'

urlpatterns = [
    path("", show_main, name="show_main"),
    path('add-toko/', create_toko, name='add_toko'),
    path('edit-toko/<int:id>/', edit_toko, name='edit_toko'),
    path('detail-toko/<int:id>/', detail_toko, name='detail_toko'),
    path('delete-toko/<int:id>/', delete_toko, name='delete_toko'),
    path('add-makanan/', add_makanan_ajax, name='add_makanan'),
    path('edit-makanan/<int:id>/', edit_makanan, name='edit_makanan'),
    path('detail-makanan/<int:id>/', detail_makanan, name='detail_makanan'),
    path('delete-makanan/<int:id>/', delete_makanan, name='delete_makanan'),
    path('makanan-json/', makanan_json, name='makanan_json'),
]