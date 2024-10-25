from django.shortcuts import render


# Create your views here.
def show_rating(request):
    context = {"test": "Test"}

    return render(request, "rating.html", context)