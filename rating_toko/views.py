from django.shortcuts import render
from .models import RumahMakan, Rating
from django.http import HttpResponse, HttpResponseRedirect
from django.core import serializers
from .forms import RatingForm
from django.utils.html import strip_tags
from django.views.decorators.http import require_POST, require_GET
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
import json
from django.urls import reverse


def get_all_toko_page(request):
    return render(request, "toko.html")


def get_all_toko(request):
    rumah_makan = RumahMakan.objects.all()
    rumah_makan_json = serializers.serialize("json", rumah_makan)

    return HttpResponse(rumah_makan_json, content_type="application/json")


def get_toko(request, id_rumah_makan):
    rumah_makan = RumahMakan.objects.get(pk=id_rumah_makan)
    rumah_makan_json = serializers.serialize("json", [rumah_makan])

    return HttpResponse(rumah_makan_json, content_type="application/json")


def get_all_ratings_page(request, id_rumah_makan):
    rumah_makan = RumahMakan.objects.get(pk=id_rumah_makan)

    context = {
        "id_rumah_makan": id_rumah_makan,
        "nama_rumah_makan": rumah_makan.nama_rumah_makan,
        "alamat": rumah_makan.alamat,
        "kota": rumah_makan.bps_nama_kabupaten_kota,
        "tahun": rumah_makan.tahun,
        "asal_masakan": rumah_makan.masakan_dari_mana,
        "id_user_session": request.user.id,
    }

    return render(request, "toko_specific.html", context)


def get_all_ratings(request, id_rumah_makan):
    ratings = Rating.objects.filter(rumah_makan=id_rumah_makan)
    ratings_json = serializers.serialize("json", ratings)

    return HttpResponse(ratings_json, content_type="application/json")


@csrf_exempt
@require_POST
@login_required(login_url="/login/")
def add_rating(request):
    # Add rating
    rating = request.POST.get("rating")
    review = strip_tags(request.POST.get("review"))
    rumah_makan = RumahMakan.objects.get(pk=request.POST.get("id_rumah_makan"))
    user = request.user
    new_rating = Rating(
        rating=rating,
        review=review,
        rumah_makan=rumah_makan,
        user=user,
    )
    new_rating.save()

    # Updating rating average
    ratings = Rating.objects.filter(rumah_makan=rumah_makan)
    new_average_rating = sum([r.rating for r in ratings]) / len(ratings)
    rumah_makan.average_rating = new_average_rating
    rumah_makan.number_of_ratings = len(ratings)
    rumah_makan.save()

    return HttpResponse(b"Rating added successfully", status=201)


@login_required(login_url="/login/")
def edit_rating(request, id_rating, id_rumah_makan):
    rating = Rating.objects.get(pk=id_rating)
    form = RatingForm(request.POST or None, instance=rating)

    if request.method == "POST":
        if form.is_valid():
            form.save()

            # Updating rating average
            rumah_makan = RumahMakan.objects.get(pk=id_rumah_makan)
            ratings = Rating.objects.filter(rumah_makan=rumah_makan)
            new_average_rating = 0
            for r in ratings:
                new_average_rating += r.rating
            new_average_rating /= len(ratings)
            rumah_makan.average_rating = new_average_rating
            rumah_makan.save()

            return HttpResponseRedirect("/rating-toko/" + str(id_rumah_makan))
    else:
        form = RatingForm(instance=rating)

    context = {
        "form": form,
        "rating": rating,
        "rumah_makan": rating.rumah_makan,
    }

    return render(request, "edit_rating.html", context)


@csrf_exempt
@login_required(login_url="/login/")
def delete_rating(request, id_rating, id_rumah_makan):
    # Delete rating
    rating = Rating.objects.get(pk=id_rating)
    rating.delete()

    # Updating rating average
    rumah_makan = RumahMakan.objects.get(pk=id_rumah_makan)
    ratings = Rating.objects.filter(rumah_makan=rumah_makan)
    new_average_rating = 0
    for r in ratings:
        new_average_rating += r.rating
    new_average_rating /= len(ratings)
    rumah_makan.average_rating = new_average_rating
    rumah_makan.number_of_ratings -= 1
    rumah_makan.save()

    return HttpResponseRedirect(
        reverse("rating_toko:get_all_ratings_page", args=[id_rumah_makan])
    )


def get_user(request, id_user):
    user = User.objects.get(pk=id_user)
    user_json = serializers.serialize("json", [user])

    return HttpResponse(user_json, content_type="application/json")
