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
import json
from django.views.decorators.http import require_http_methods


# Create your views here.

def forum_main(request):
    forums = Discussion.objects.all()

    context = {
        'title': "test forum",
        'forums': forums
    }

    return render(request, "forum.html", context)

def api_forum_main(request):
    data = Discussion.objects.all()
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")

def api_forum_by_id(request, id):
    data = Discussion.objects.filter(pk=id)
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")

from django.views.decorators.csrf import csrf_exempt
import json
from django.http import JsonResponse

@csrf_exempt
def api_create_forum(request):
    if request.method == 'POST':
        data = json.loads(request.body)

        # Jika user belum login, misal assign default user atau tolak:
        if request.user.is_anonymous:
            return JsonResponse({"status": "error", "message": "User is not authenticated."}, status=401)

        new_forum = Discussion.objects.create(
            user=request.user,
            title=data["title"],
            content=data["content"]
        )
        new_forum.save()

        return JsonResponse({"status": "success"}, status=200)
    else:
        return JsonResponse({"status": "error", "message": "Method not allowed"}, status=405)

@require_POST
@login_required
def add_forum_topic_ajax(request):
    title = request.POST.get('title', '').strip()
    content = request.POST.get('content', '').strip()

    if title and content:
        # Create a new Discussion instance and save it to the database
        discussion = Discussion.objects.create(
            user=request.user,
            title=title,
            content=content
        )

        # Prepare the data to be sent back in the response
        discussion_data = {
            'id': str(discussion.id),  # Convert UUID to string
            'title': discussion.title,
            'content': discussion.content,
            'user': {
                'id': discussion.user.id,
                'username': discussion.user.username,
            },
            'date_created': discussion.date_created.strftime('%Y-%m-%d %H:%M:%S'),
        }

        # Return a JSON response with the discussion data and a 201 status code
        return JsonResponse({'discussion': discussion_data}, status=201)
    else:
        # Return an error if title or content is missing
        return JsonResponse({'error': 'Title and content are required.'}, status=400)

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

@require_http_methods(["POST"])
@login_required
def edit_forum_ajax(request, id):
    # Ambil diskusi berdasarkan id
    discussion = get_object_or_404(Discussion, pk=id)

    # Periksa apakah pengguna saat ini adalah pemilik diskusi
    if discussion.user != request.user:
        return JsonResponse({'error': 'Anda tidak diizinkan untuk mengedit forum ini.'}, status=403)

    # Parse data JSON dari request body
    try:
        data = json.loads(request.body)
        title = data.get('title', '').strip()
        content = data.get('content', '').strip()
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Data JSON tidak valid.'}, status=400)

    if title and content:
        # Update diskusi
        discussion.title = title
        discussion.content = content
        discussion.save()

        # Siapkan data untuk dikirim kembali dalam respons
        discussion_data = {
            'id': str(discussion.id),
            'title': discussion.title,
            'content': discussion.content,
            'user': {
                'id': discussion.user.id,
                'username': discussion.user.username,
            },
            'date_created': discussion.date_created.strftime('%Y-%m-%d %H:%M:%S'),
        }

        return JsonResponse({'discussion': discussion_data}, status=200)
    else:
        return JsonResponse({'error': 'Title and content are required.'}, status=400)

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




def discussion_main(request, id):
    # Mengambil diskusi berdasarkan ID atau mengembalikan 404 jika tidak ditemukan
    discussion = get_object_or_404(Discussion, pk=id)
    
    # Mengambil komentar tingkat atas (tanpa parent), prefetch replies dan likes
    comments = discussion.comments.select_related('user').prefetch_related('replies', 'likes').filter(parent__isnull=True).annotate(num_likes=Count('likes')).order_by('-num_likes', '-date_created')

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

@require_http_methods(["POST"])
@login_required
def edit_comment_ajax(request, id):
    # Ambil komentar berdasarkan id
    comment = get_object_or_404(Comment, pk=id)

    # Periksa apakah pengguna saat ini adalah pemilik komentar
    if comment.user != request.user:
        return JsonResponse({'error': 'Anda tidak diizinkan untuk mengedit komentar ini.'}, status=403)

    # Parse data JSON dari request body
    try:
        data = json.loads(request.body)
        content = data.get('content', '').strip()
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Data JSON tidak valid.'}, status=400)

    if content:
        # Update komentar
        comment.content = content
        comment.save()

        # Siapkan data untuk dikirim kembali dalam respons
        comment_data = {
            'id': str(comment.id),
            'content': comment.content,
            'user': {
                'id': comment.user.id,
                'username': comment.user.username,
            },
            'date_created': comment.date_created.strftime('%Y-%m-%d %H:%M:%S'),
        }

        return JsonResponse({'comment': comment_data}, status=200)
    else:
        return JsonResponse({'error': 'Content is required.'}, status=400)
    
@login_required
def add_comment(request, id):
    discussion = get_object_or_404(Discussion, pk=id)
    
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            parent_id = request.POST.get('parent_id')  # Mengambil parent_id jika ada
            new_comment = form.save(commit=False)
            new_comment.user = request.user
            new_comment.discussion = discussion
            if parent_id:
                parent_comment = get_object_or_404(Comment, pk=parent_id)
                new_comment.parent = parent_comment
            new_comment.save()
            return redirect('discuss_forum:discussion_main', id=discussion.id)
    else:
        form = CommentForm()
    
    context = {
        'discussion': discussion,
        'form': form,
    }
    return render(request, "discussion.html", context)