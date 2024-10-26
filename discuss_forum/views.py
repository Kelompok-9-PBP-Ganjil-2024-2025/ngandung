from django.shortcuts import render, redirect, get_object_or_404
from discuss_forum.models import Discussion, Comment
from discuss_forum.forms import DiscussionForm
from django.http import HttpResponse
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required

# Create your views here.

def forum_main(request):
    forums = Discussion.objects.all()

    context = {
        'title': "test forum",
        'forums': forums
    }

    return render(request, "forum.html", context)

def discussion_main(request, id):

    # Mengambil diskusi berdasarkan ID dan akan mengembalikan 404 jika ID tidak ditemukan.
    discussion = get_object_or_404(Discussion, pk=id)

    discuss = Comment.objects.all().order_by('-date_created') # Komentar terbaru

    context = {
        'content': "WOI GUA SETUJU BANGET, ITU ENAK BANGET",
        'discuss': discuss,
        'discussion': discussion,
    }

    return render(request, "discussion.html", context)

@login_required
def create_discussion_forum(request):
    form = DiscussionForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        # Buat objek tetapi tidak langsung menyimpan ke database
        new_forum = form.save(commit=False)
        # Tetapkan user dari request ke objek forum baru
        new_forum.user = request.user
        # Simpan objek ke database
        new_forum.save()
        return redirect('discuss_forum:forum_main')

    context = {'form': form}
    return render(request, "create_discuss_forum.html", context)


def show_json(request):
    data = Discussion.objects.all()
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")

def show_json_by_id(request, id):
    data = Discussion.objects.filter(pk=id)
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")

@csrf_exempt
@require_POST
def add_forum_topic_ajax(request):
    title = request.POST.get("title")
    content = request.POST.get("content")
    user = request.user

    new_forum = Discussion(
        title=title, content=content,
        user=user
    )
    new_forum.save()

    return HttpResponse(b"CREATED", status=201)