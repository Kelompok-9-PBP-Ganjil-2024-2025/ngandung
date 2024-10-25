from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.core import serializers
from toko_makanan.models import Toko, Makanan
from toko_makanan.forms import FormToko, FormMakanan
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.utils.html import strip_tags
# Create your views here.
#*=========================================================================================================================================
def show_main(req):
    toko = Toko.objects.all()
    context = {
        'list_toko': toko
    }
    return render(req, "mainPage/index.html", context)
#*=========================================================================================================================================
@login_required(login_url='/login')
def create_toko(req):
    form = FormToko(req.POST or None, req.FILES)

    if form.is_valid() and req.method == "POST":
        toko = form.save(commit=False)
        toko.save()
        return redirect('toko_makanan:show_main')

    context = {'form': form}
    return render(req, "addToko/index.html", context)

#*=========================================================================================================================================
@login_required(login_url='/login')
def edit_toko(req, id):
    toko = Toko.objects.get(pk=id)

    if req.method == "POST":
        form = FormToko(req.POST or None, req.FILES or None, instance=toko)
        if form.is_valid() :
            form.save()
            return HttpResponseRedirect(reverse('toko_makanan:show_main'))
    
    context = {'form': form}
    return render(req, "editToko/index.html", context)
#*=========================================================================================================================================
@login_required(login_url='/login')
def delete_toko(req, id):
    toko = Toko.objects.get(pk=id)
    toko.delete()
    return HttpResponseRedirect(reverse('toko_makanan:show_main'))
#*=========================================================================================================================================
def detail_toko(req, id):
    toko = get_object_or_404(Makanan, pk=id)
    context = {'toko': toko}
    return render(req, 'detailToko/index.html', context)
#*=========================================================================================================================================
@login_required(login_url='/login')
@csrf_exempt #dengan menggunakan ini Django tidak perlu mengecek keberadaan csrf_token pada POST request yang dikirimkan ke fungsi ini.
@require_POST #membuat fungsi hanya bisa diakses ketika pengguna mengirimkan POST request ke fungsi tersebut
def add_makanan_ajax(req):
    try:
        # Ambil data dari request POST
        nama = strip_tags(req.POST.get("nama"))
        harga = req.POST.get("harga")
        toko_id = req.POST.get('toko')

        # Cari toko berdasarkan ID
        try:
            toko = Toko.objects.get(id=toko_id)
        except Toko.DoesNotExist:
            return JsonResponse({"error": "Toko tidak ditemukan"}, status=400)

        # Buat Makanan baru
        new_product = Makanan(
            nama=nama,
            harga=harga,
            toko=toko, 
        )

        # Simpan produk baru
        new_product.save()

        return JsonResponse({"message": "Makanan berhasil ditambahkan"}, status=201)

    except Exception as e:
        # Menangani error tak terduga
        return JsonResponse({"error": str(e)}, status=500)
#*=========================================================================================================================================
@login_required(login_url='/login')
def edit_makanan(req, id):
    makanan = Makanan.objects.get(pk=id)

    if req.method == "POST":
        form = FormMakanan(req.POST or None, req.FILES or None, instance=makanan)
        if form.is_valid() :
            form.save()
            return HttpResponseRedirect(reverse('toko_makanan:show_main'))
    
    context = {'form': form}
    return render(req, "editMakanan/index.html", context)
#*=========================================================================================================================================
@login_required(login_url='/login')
def delete_makanan(req, id):
    makanan = Makanan.objects.get(pk=id)
    makanan.delete()
    return HttpResponseRedirect(reverse('toko_makanan:show_main'))
#*=========================================================================================================================================
def detail_makanan(req, id):
    makanan = get_object_or_404(Makanan, pk=id)
    context = {'makanan': makanan}
    return render(req, 'detailMakanan/index.html', context)
#*=========================================================================================================================================
def makanan_json(req):
    data = Makanan.objects.all()
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")