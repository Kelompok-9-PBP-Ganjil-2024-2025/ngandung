from django.urls import path
from toko_makanan.views import *

app_name = 'toko_makanan'

urlpatterns = [
    path("", show_main, name="show_main"),
    path('add-toko/', create_toko, name='add_toko'),
    path('edit-toko/<uuid:id>/', edit_toko, name='edit_toko'),
    path('detail-toko/<uuid:id>/', detail_toko, name='detail_toko'),
    path('delete-toko/<uuid:id>/', delete_toko, name='delete_toko'),
    path('add-makanan/', add_makanan_ajax, name='add_makanan'),
    path('edit-makanan/<uuid:id>/', edit_makanan, name='edit_makanan'),
    path('detail-makanan/<uuid:id>/', detail_makanan, name='detail_makanan'),
    path('delete-makanan/<uuid:id>/', delete_makanan, name='delete_makanan'),
    path('makanan-json/', makanan_json, name='makanan_json'),
]