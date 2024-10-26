from django.shortcuts import render
from main.models import *
from .models import UserProfile
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from .models import UserProfile


# Create your views here.
def show_main(request):
    context = {
        'test' : 'Test'
    }

    return render(request, "main.html", context)

def tambah_ke_favorit(request, toko_id):
    user_profile = get_object_or_404(UserProfile, user=request.user)
    toko = get_object_or_404(RumahMakan, id=toko_id)
    user_profile.favorit_toko.add(toko)
    return redirect('dev_favorite_store:daftar_favorit')

def hapus_dari_favorit(request, toko_id):
    user_profile = get_object_or_404(UserProfile, user=request.user)
    toko = get_object_or_404(RumahMakan, id=toko_id)
    user_profile.favorit_toko.remove(toko)
    return redirect('dev_favorite_store:daftar_favorit')

@login_required(login_url='/login/')
def daftar_favorit(request):
    if not request.user.is_authenticated:
        messages.info(request, 'Login dulu agar bisa mengakses halaman ini.')
        return redirect('/login')  # Ganti dengan URL login kamu
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)
    favorit_toko = user_profile.favorit_toko.all()  # Ambil toko favorit user
    print(f"Favorit Toko: {favorit_toko}")
    return render(request, 'daftar_favorit.html', {'favorit_toko': favorit_toko})
