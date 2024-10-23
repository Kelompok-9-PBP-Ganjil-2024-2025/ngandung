import datetime
from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.core import serializers
from django.urls import reverse
from tambah_toko_makanan.models import Toko, Makanan
from tambah_toko_makanan.forms import FormToko, FormMakanan
# Create your views here.
#*=========================================================================================================================================
def create_toko(req):
    form = FormToko(req.POST or None, req.FILES)

    if form.is_valid() and req.method == "POST":
        toko = form.save(commit=False)
        toko.save()
        return redirect('main:show_main')

    context = {'form': form}
    return render(req, "addToko/index.html", context)
#*=========================================================================================================================================
def edit_toko(req, id):
    toko = Toko.objects.get(pk=id)

    if req.method == "POST":
        form = FormToko(req.POST or None, req.FILES or None, instance=toko)
        if form.is_valid() :
            form.save()
            return HttpResponseRedirect(reverse('main:show_main'))
    
    context = {'form': form}
    return render(req, "editToko/index.html", context)
#*=========================================================================================================================================
def delete_toko(req, id):
    toko = Toko.objects.get(pk=id)
    toko.delete()
    return HttpResponseRedirect(reverse('main:show_main'))
#*=========================================================================================================================================
def detail_toko(req, id):
    toko = get_object_or_404(Makanan, pk=id)
    context = {'toko': toko}
    return render(req, 'detailToko/index.html', context)
#*=========================================================================================================================================
def create_makanan(req):
    form = FormMakanan(req.POST or None, req.FILES)

    if form.is_valid() and req.method == "POST":
        makanan = form.save(commit=False)
        makanan.save()
        return redirect('main:show_main')

    context = {'form': form}
    return render(req, "addMakanan/index.html", context)
#*=========================================================================================================================================
def edit_makanan(req, id):
    makanan = Makanan.objects.get(pk=id)

    if req.method == "POST":
        form = FormMakanan(req.POST or None, req.FILES or None, instance=makanan)
        if form.is_valid() :
            form.save()
            return HttpResponseRedirect(reverse('main:show_main'))
    
    context = {'form': form}
    return render(req, "editMakanan/index.html", context)
#*=========================================================================================================================================
def delete_makanan(req, id):
    makanan = Makanan.objects.get(pk=id)
    makanan.delete()
    return HttpResponseRedirect(reverse('main:show_main'))
#*=========================================================================================================================================
def detail_makanan(req, id):
    makanan = get_object_or_404(Makanan, pk=id)
    context = {'makanan': makanan}
    return render(req, 'detailMakanan/index.html', context)