from django.shortcuts import render
from main.models import Makanan, Toko, UserProfile
from django.shortcuts import get_object_or_404, redirect


# Create your views here.
def show_main(request):
    context = {
        'test' : 'Test'
    }

    return render(request, "main.html", context)

def tambah_ke_favorit(request, toko_id):
    user_profile = get_object_or_404(UserProfile, user=request.user)
    toko = get_object_or_404(Toko, id=toko_id)
    user_profile.favorit_toko.add(toko)
    return redirect('daftar_favorit')
