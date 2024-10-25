from django.shortcuts import render
from .models import RumahMakan
from django.http import HttpResponse, HttpResponseRedirect
from django.core import serializers

def show_main(request):
    context = {"test": "Test"}

    return render(request, "main.html", context)


def show_rumah_makan_json_by_id(request, id):
    rumah_makan = RumahMakan.objects.filter(pk=id)

    return HttpResponse(
        serializers.serialize("json", rumah_makan), content_type="application/json"
    )
