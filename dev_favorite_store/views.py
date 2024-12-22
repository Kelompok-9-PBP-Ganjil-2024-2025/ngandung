from django.shortcuts import render
from main.models import *
from .models import Favorite
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
import json
from django.http import JsonResponse
from django.http import JsonResponse, HttpResponseBadRequest

def show_main(request):
    context = {
        'test': 'Test'
    }
    return render(request, "main.html", context)

@csrf_exempt
@login_required(login_url="/login/")
def tambah_ke_favorite(request, rumah_makan_id):
    if request.method == 'POST':
        try:
            if not rumah_makan_id:
                return JsonResponse({"status": "error", "message": "ID rumah makan tidak ditemukan"}, status=400)

            rumah_makan = get_object_or_404(RumahMakan, pk=rumah_makan_id)
            user = request.user

            # Check if the restaurant is already a favorite
            favorite, created = Favorite.objects.get_or_create(rumah_makan=rumah_makan, user=user)

            if created:
                return JsonResponse({"status": "added", "message": "Restoran ditambahkan ke favorit"}, status=201)
            else:
                return JsonResponse({"status": "exists", "message": "Restoran sudah ada di favorit"}, status=200)

        except json.JSONDecodeError:
            return JsonResponse({"status": "error", "message": "Bad JSON format"}, status=400)
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=500)

    return JsonResponse({"status": "error", "message": "Invalid request method"}, status=405)

@login_required
def hapus_dari_favorit(request, toko_id):
    if request.method == 'POST':
        try:
            user = request.user
            toko = get_object_or_404(RumahMakan, id=toko_id)

            # Cari favorite yang sesuai dan hapus jika ada
            favorite = Favorite.objects.filter(user=user, rumah_makan=toko).first()
            if favorite:
                favorite.delete()
                return JsonResponse({'status': 'success', 'message': 'Toko berhasil dihapus dari favorit.'}, status=200)
            else:
                return JsonResponse({'status': 'error', 'message': 'Toko tidak ditemukan di favorit.'}, status=404)

        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
    else:
        return HttpResponseBadRequest('Invalid request method.')

@login_required(login_url='/login/')
def daftar_favorit(request):
    # Ambil semua entri Favorite milik user yang sedang login
    favorit_toko = Favorite.objects.filter(user=request.user).select_related('rumah_makan')

    # Ambil objek RumahMakan dari setiap Favorite agar dapat ditampilkan di template
    daftar_favorit_toko = [fav.rumah_makan for fav in favorit_toko]

    # Render halaman dengan daftar toko favorit
    return render(request, 'daftar_favorit.html', {'favorit_toko': daftar_favorit_toko})

# Endpoint API untuk menampilkan daftar restoran favorit user
def user_favorite_restaurants(request):
    user = request.user
    favorites = Favorite.objects.filter(user=user).select_related('rumah_makan')

    data = []
    for favorite in favorites:
        rm = favorite.rumah_makan
        data.append({
            'id': favorite.id,
            'rumah_makan': {
                'id': rm.id,
                'kode_provinsi': rm.kode_provinsi,
                'nama_provinsi': rm.nama_provinsi,
                'bps_kode_kabupaten_kota': rm.bps_kode_kabupaten_kota,
                'bps_nama_kabupaten_kota': rm.bps_nama_kabupaten_kota,
                'nama_rumah_makan': rm.nama_rumah_makan,
                'alamat': rm.alamat,
                'latitude': float(rm.latitude),
                'longitude': float(rm.longitude),
                'tahun': rm.tahun,
                'masakan_dari_mana': rm.masakan_dari_mana,
                'makanan_berat_ringan': rm.makanan_berat_ringan,
            }
        })

    return JsonResponse(data, safe=False)

# Hapus fav flutter
@csrf_exempt
@login_required
def delete_favorite(request, favorite_id):
    if request.method == 'POST':
        try:
            favorite = Favorite.objects.get(id=favorite_id, user=request.user)
            favorite.delete()
            return JsonResponse({'message': 'Favorite deleted successfully'}, status=200)
        except Favorite.DoesNotExist:
            return JsonResponse({'error': 'Favorite not found'}, status=404)
    return JsonResponse({'error': 'Invalid method'}, status=405)

# Tambah fav flutter
@csrf_exempt
@login_required
def add_to_favorite(request):
    if request.method == 'POST':
        try:
            body = json.loads(request.body)
            rumah_makan_id = body.get('rumah_makan_id')

            if not rumah_makan_id:
                return JsonResponse({"status": "error", "message": "ID rumah makan tidak ditemukan"}, status=400)

            rumah_makan = get_object_or_404(RumahMakan, pk=rumah_makan_id)
            user = request.user

            # Add to favorite
            favorite, created = Favorite.objects.get_or_create(rumah_makan=rumah_makan, user=user)
            if created:
                return JsonResponse({"status": "success", "message": "Restoran berhasil ditambahkan ke favorit"}, status=201)
            else:
                return JsonResponse({"status": "exists", "message": "Restoran sudah ada di favorit"}, status=200)

        except json.JSONDecodeError:
            return JsonResponse({"status": "error", "message": "Bad JSON format"}, status=400)
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=500)

    return JsonResponse({"status": "error", "message": "Invalid request method"}, status=405)
