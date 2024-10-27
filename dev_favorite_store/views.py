from django.shortcuts import render
from toko_makanan.models import *
from .models import Favorite
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
import json
from django.http import JsonResponse


 
from django.http import JsonResponse, HttpResponseBadRequest


# Create your views here.
def show_main(request):
    context = {
        'test' : 'Test'
    }

    return render(request, "main.html", context)

# def tambah_ke_favorit(request, toko_id):
#     user_profile = get_object_or_404(UserProfile, user=request.user)
#     toko = get_object_or_404(RumahMakan, id=toko_id)
#     user_profile.favorit_toko.add(toko)
#     return redirect('dev_favorite_store:daftar_favorit')

@csrf_exempt
@login_required(login_url="/login/")
def tambah_ke_favorite(request):
    if request.method == 'POST':
        try:
            # Parsing JSON body
            data = json.loads(request.body)
            rumah_makan_id = data.get("rumah_makan_id")

            if not rumah_makan_id:
                return JsonResponse({"status": "error", "message": "ID rumah makan tidak ditemukan"}, status=400)

            rumah_makan = get_object_or_404(RumahMakan, pk=rumah_makan_id)
            user = request.user

            # Check if the restaurant is already a favorite
            favorite, created = Favorite.objects.get_or_create(rumah_makan=rumah_makan, user=user)

            if created:
                return JsonResponse({"status": "added", "message": "Restoran ditambahkan ke favorit"}, status=201)
            else:
                favorite.delete()
                return JsonResponse({"status": "removed", "message": "Restoran dihapus dari favorit"}, status=200)

        except json.JSONDecodeError:
            return JsonResponse({"status": "error", "message": "Bad JSON format"}, status=400)
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=500)

    return JsonResponse({"status": "error", "message": "Invalid request method"}, status=405)

# @login_required
# def hapus_dari_favorit(request, toko_id):
#     if request.method == 'POST':
#         try:
#             user_profile = get_object_or_404(UserProfile, user=request.user)
#             toko = get_object_or_404(RumahMakan, id=toko_id)
#             user_profile.favorit_toko.remove(toko)
#             return JsonResponse({'status': 'success', 'message': 'Toko berhasil dihapus dari favorit.'}, status=200)
#         except Exception as e:
#             return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
#     else:
#         return HttpResponseBadRequest('Invalid request method.')

@login_required
def hapus_dari_favorit(request, toko_id):
    if request.method == 'POST':
        try:
            user = request.user
            toko = get_object_or_404(RumahMakan, id=toko_id)
            
            # Cari favorite yang sesuai dan hapus jika ada
            favorite = Favorite.objects.filter(user=user, rumah_makan=toko)
            if favorite.exists():
                favorite.delete()
                return JsonResponse({'status': 'success', 'message': 'Toko berhasil dihapus dari favorit.'}, status=200)
            else:
                return JsonResponse({'status': 'error', 'message': 'Toko tidak ditemukan di favorit.'}, status=404)

        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
    else:
        return HttpResponseBadRequest('Invalid request method.')

@login_required(login_url='/login/')
@login_required(login_url='/login/')
def daftar_favorit(request):
    # Ambil semua entri Favorite milik user yang sedang login
    favorit_toko = Favorite.objects.filter(user=request.user).select_related('rumah_makan')

    # Ambil objek RumahMakan dari setiap Favorite agar dapat ditampilkan di template
    daftar_favorit_toko = [fav.rumah_makan for fav in favorit_toko]

    # Render halaman dengan daftar toko favorit
    return render(request, 'daftar_favorit.html', {'favorit_toko': daftar_favorit_toko})


