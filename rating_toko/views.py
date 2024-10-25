from django.shortcuts import render
from .models import RumahMakan
from django.http import HttpResponse, HttpResponseRedirect
from django.core import serializers

# Create your views here.
def show_rating(request):
    context = {"test": "Test"}

    return render(request, "rating.html", context)

def show_rating_detail_json(request, id):
    rumah_makan = RumahMakan.objects.filter(pk=id)

    return HttpResponse(
        serializers.serialize("json", rumah_makan), content_type="application/json"
    )
