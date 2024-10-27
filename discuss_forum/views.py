from django.shortcuts import render, redirect, get_object_or_404, reverse
from discuss_forum.models import Discussion, Comment
from discuss_forum.forms import DiscussionForm, CommentForm
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.http import JsonResponse



# Create your views here.

def forum_main(request):
    forums = Discussion.objects.all()

    context = {
        'title': "test forum",
        'forums': forums
    }

    return render(request, "forum.html", context)

def discussion_main(request, id):
    # Mengambil diskusi berdasarkan ID atau mengembalikan 404 jika tidak ditemukan
    discussion = get_object_or_404(Discussion, pk=id)
    
    # Mengambil semua komentar terkait diskusi, urutkan terbaru terlebih dahulu
    comments = discussion.comments.annotate(num_likes=Count('likes')).order_by('-num_likes', '-date_created')

    context = {
        'discussion': discussion,
        'comments': comments,
    }

    return render(request, "discussion.html", context)

# Jika Anda menambahkan fitur komentar
@login_required
def add_comment(request, id):
    discussion = get_object_or_404(Discussion, pk=id)
    
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.user = request.user
            new_comment.discussion = discussion
            new_comment.save()
            return redirect('discuss_forum:discussion_main', id=discussion.id)
    else:
        form = CommentForm()
    
    context = {
        'discussion': discussion,
        'form': form,
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

@login_required
def edit_forum(request, id):
    # Ambil diskusi berdasarkan id atau kembalikan 404 jika tidak ditemukan
    discussion = get_object_or_404(Discussion, pk=id)
    
    # Periksa apakah pengguna saat ini adalah pemilik diskusi
    if discussion.user != request.user:
        return HttpResponseForbidden("Anda tidak diizinkan untuk mengedit forum ini.")
    
    # Gunakan DiscussionForm untuk membuat form
    form = DiscussionForm(request.POST or None, instance=discussion)
    
    if form.is_valid() and request.method == "POST":
        form.save()
        return redirect('discuss_forum:forum_main')
    
    context = {'form': form}
    return render(request, "edit_forum.html", context)

@login_required
def delete_forum(request, id):
    discussion = get_object_or_404(Discussion, pk=id)
    
    if discussion.user != request.user:
        return HttpResponseForbidden("Anda tidak diizinkan untuk menghapus forum ini.")
    
    if request.method == "POST":
        discussion.delete()
        return redirect('discuss_forum:forum_main')
    
    context = {'discussion': discussion}
    return render(request, "confirm_delete.html", context)

@login_required
def edit_comment(request, id):
    # Ambil komentar berdasarkan id atau kembalikan 404 jika tidak ditemukan
    comment = get_object_or_404(Comment, pk=id)
    
    # Periksa apakah pengguna saat ini adalah pemilik komentar
    if comment.user != request.user:
        return HttpResponseForbidden("Anda tidak diizinkan untuk mengedit komentar ini.")
    
    # Gunakan CommentForm untuk membuat form
    form = CommentForm(request.POST or None, instance=comment)
    
    if form.is_valid() and request.method == "POST":
        form.save()
        return redirect('discuss_forum:discussion_main', id=comment.discussion.id)
    
    context = {'form': form}
    return render(request, "edit_comment.html", context)

@login_required
def delete_comment(request, id):
    comment = get_object_or_404(Comment, pk=id)
    
    if comment.user != request.user:
        return HttpResponseForbidden("Anda tidak diizinkan untuk menghapus komentar ini.")
    
    if request.method == "POST":
        discussion_id = comment.discussion.id
        comment.delete()
        return redirect('discuss_forum:discussion_main', id=discussion_id)
    
    context = {'comment': comment}
    return render(request, "delete_comment.html", context)

@login_required
def like_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    if request.user in comment.likes.all():
        comment.likes.remove(request.user)
        liked = False
    else:
        comment.likes.add(request.user)
        liked = True
    
    # Menghitung total likes setelah perubahan
    total_likes = comment.likes.count()
    
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({
            'liked': liked,
            'total_likes': total_likes
        })
    else:
        # Redirect ke halaman diskusi yang sama jika bukan AJAX
        return redirect(reverse('discuss_forum:discussion_main', args=[comment.discussion.id]))
