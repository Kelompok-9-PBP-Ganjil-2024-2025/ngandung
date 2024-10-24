from django.shortcuts import render

# Create your views here.


def forum_main(request):

    context = {
        'title': "test forum",
    }

    return render(request, "forum.html", context)