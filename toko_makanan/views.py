from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from toko_makanan.models import Toko, Makanan
from toko_makanan.forms import FormToko, FormMakanan
from django.contrib.auth.decorators import login_required
# Create your views here.
#*=========================================================================================================================================
def show_main(req):
    makanan = Makanan.objects.all()
    context = {
        'makanan': makanan
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
def create_makanan(req):
    form = FormMakanan(req.POST or None, req.FILES)

    if form.is_valid() and req.method == "POST":
        makanan = form.save(commit=False)
        makanan.save()
        return redirect('toko_makanan:show_main')

    context = {'form': form}
    return render(req, "addMakanan/index.html", context)
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