from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.core import serializers
from toko_makanan.models import RumahMakan, Makanan
from toko_makanan.forms import FormRumahMakan, FormMakanan
from django.db.models import Min, Max
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.utils.html import strip_tags
# Create your views here.
#*=========================================================================================================================================
def show_main(req):
    rumah_makan = RumahMakan.objects.all()
    context = {
        'list_rumah_makan': rumah_makan
    }
    return render(req, "mainPage/index.html", context)
#*=========================================================================================================================================
@login_required(login_url='/login')
def create_toko(req):
    form = FormRumahMakan(req.POST or None, req.FILES)

    if form.is_valid() and req.method == "POST":
        toko = form.save(commit=False)
        toko.save()
        return redirect('toko_makanan:show_main')

    context = {'form': form}
    return render(req, "addRumahMakan/index.html", context)
#*=========================================================================================================================================
@login_required(login_url='/login')
def edit_toko(req, id):
    toko = RumahMakan.objects.get(pk=id)
    form = FormRumahMakan(req.POST or None, req.FILES or None, instance=toko)
    if req.method == "POST" and form.is_valid() :
        form.save()
        return HttpResponseRedirect(reverse('toko_makanan:show_main'))
    
    context = {'form': form}
    return render(req, "editRumahMakan/index.html", context)
#*=========================================================================================================================================
@login_required(login_url='/login')
def delete_toko(req, id):
    toko = RumahMakan.objects.get(pk=id)
    toko.delete()
    return HttpResponseRedirect(reverse('toko_makanan:show_main'))
#*=========================================================================================================================================
@login_required(login_url='/login')
@csrf_exempt #dengan menggunakan ini Django tidak perlu mengecek keberadaan csrf_token pada POST request yang dikirimkan ke fungsi ini.
@require_POST #membuat fungsi hanya bisa diakses ketika pengguna mengirimkan POST request ke fungsi tersebut
def add_makanan_ajax(req):
    try:
        name = strip_tags(req.POST.get("name"))
        price = req.POST.get("price")
        toko_id = req.POST.get('toko_id')

        try:
            toko = RumahMakan.objects.get(id=toko_id)
        except RumahMakan.DoesNotExist:
            return JsonResponse({"error": "Rumah Makan tidak ditemukan"}, status=400)

        new_product = Makanan(
            name=name,
            price=price,
            rumah_makan=toko, 
        )
        new_product.save()

        return JsonResponse({"message": "Makanan berhasil ditambahkan"}, status=201)

    except Exception as e:
        # Menangani error tak terduga
        return JsonResponse({"error": str(e)}, status=500)
#*=========================================================================================================================================
@login_required(login_url='/login')
def edit_makanan(req, id):
    makanan = Makanan.objects.get(pk=id)
    form = FormMakanan(req.POST or None, req.FILES or None, instance=makanan)
    if form.is_valid() and req.method == "POST":
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
def detail_rumah_makan(req, id):
    makanan = get_object_or_404(Makanan, pk=id)
    rumah_makan = makanan.rumah_makan
    list_makanan = rumah_makan.makanan.all()
    price_range = list_makanan.aggregate(min_price=Min('price'), max_price=Max('price'))
    tipe_makanan = rumah_makan.makanan_berat_ringan
    gmap_url = f"https://maps.google.com/?q={rumah_makan.latitude},{rumah_makan.longitude}"
    context = {
        'rumah_makan': rumah_makan,
        'list_makanan': list_makanan,
        'min_price' : price_range['min_price'],
        'max_price': price_range['max_price'],
        'tipe_makanan': tipe_makanan,
        'gmap_url': gmap_url,
        }
    return render(req, 'detailRumahMakan/index.html', context)
#*=========================================================================================================================================
def makanan_json(req):
    data = Makanan.objects.all()
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")