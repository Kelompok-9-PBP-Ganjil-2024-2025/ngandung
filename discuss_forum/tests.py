from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import User
from django.core import serializers
from django.http import JsonResponse
from django.db.models import Count
from django.conf import settings
from .models import MoodEntry
from discuss_forum.models import Discussion, Comment
from discuss_forum.forms import DiscussionForm, CommentForm
import json

# ============================
# Tests untuk Fitur Utama
# ============================

class MainSiteTests(TestCase):
    def setUp(self):
        self.client = Client()
    
    def test_main_url_exists(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
    
    def test_main_template_used(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'main.html')
    
    def test_nonexistent_page(self):
        response = self.client.get('/skibidi/')
        self.assertEqual(response.status_code, 404)
    
    def test_strong_mood_user(self):
        now = timezone.now()
        mood = MoodEntry.objects.create(
            mood="LUMAYAN SENANG",
            time=now,
            feelings="senang sih, cuman tadi baju aku basah kena hujan :(",
            mood_intensity=8,
        )
        self.assertTrue(mood.is_mood_strong)

# ============================
# Tests untuk Aplikasi Discuss Forum
# ============================

class DiscussForumTests(TestCase):
    def setUp(self):
        # Membuat pengguna untuk pengujian
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client = Client()
        self.client.login(username='testuser', password='testpass')
        
        # Membuat diskusi contoh
        self.discussion = Discussion.objects.create(
            user=self.user,
            title="Diskusi Test",
            content="Konten diskusi test."
        )
        
        # Membuat komentar contoh
        self.comment = Comment.objects.create(
            discussion=self.discussion,
            user=self.user,
            content="Komentar test."
        )
    
    def test_forum_main_view(self):
        response = self.client.get(reverse('discuss_forum:forum_main'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'forum.html')
        self.assertContains(response, "test forum")
        self.assertContains(response, self.discussion.title)
    
    def test_discussion_main_view(self):
        response = self.client.get(reverse('discuss_forum:discussion_main', args=[self.discussion.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'discussion.html')
        self.assertContains(response, self.discussion.title)
        self.assertContains(response, self.comment.content)
    
    def test_create_discussion_view(self):
        response = self.client.post(reverse('discuss_forum:create_discussion_forum'), {
            'title': 'Diskusi Baru',
            'content': 'Konten diskusi baru.'
        })
        self.assertEqual(response.status_code, 302)  # Redirect setelah berhasil
        self.assertTrue(Discussion.objects.filter(title='Diskusi Baru').exists())
    
    def test_add_comment_view(self):
        response = self.client.post(reverse('discuss_forum:add_comment', args=[self.discussion.id]), {
            'content': 'Komentar baru.'
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Comment.objects.filter(content='Komentar baru.').exists())
    
    def test_edit_discussion_view(self):
        response = self.client.post(reverse('discuss_forum:edit_forum', args=[self.discussion.id]), {
            'title': 'Diskusi Diedit',
            'content': 'Konten diskusi yang sudah diedit.'
        })
        self.assertEqual(response.status_code, 302)
        self.discussion.refresh_from_db()
        self.assertEqual(self.discussion.title, 'Diskusi Diedit')
    
    def test_delete_discussion_view(self):
        response = self.client.post(reverse('discuss_forum:delete_forum', args=[self.discussion.id]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Discussion.objects.filter(id=self.discussion.id).exists())
    
    def test_like_comment_view(self):
        like_url = reverse('discuss_forum:like_comment', args=[self.comment.id])
        response = self.client.post(like_url, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertTrue(data['liked'])
        self.assertEqual(data['total_likes'], 1)
        
        # Menguji pembatalan like
        response = self.client.post(like_url, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        data = json.loads(response.content)
        self.assertFalse(data['liked'])
        self.assertEqual(data['total_likes'], 0)
    
    def test_show_json_view(self):
        response = self.client.get(reverse('discuss_forum:show_json'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/json')
        data = json.loads(response.content)
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['fields']['title'], self.discussion.title)
    
    def test_edit_forum_ajax_view(self):
        edit_url = reverse('discuss_forum:edit_forum_ajax', args=[self.discussion.id])
        response = self.client.post(edit_url, json.dumps({
            'title': 'Diskusi AJAX Diedit',
            'content': 'Konten diskusi AJAX yang sudah diedit.'
        }), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(data['discussion']['title'], 'Diskusi AJAX Diedit')
        self.discussion.refresh_from_db()
        self.assertEqual(self.discussion.title, 'Diskusi AJAX Diedit')
    
    def test_edit_comment_ajax_view(self):
        edit_url = reverse('discuss_forum:edit_comment_ajax', args=[self.comment.id])
        response = self.client.post(edit_url, json.dumps({
            'content': 'Komentar AJAX yang diedit.'
        }), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(data['comment']['content'], 'Komentar AJAX yang diedit.')
        self.comment.refresh_from_db()
        self.assertEqual(self.comment.content, 'Komentar AJAX yang diedit.')
    
    def test_permission_edit_discussion(self):
        # Membuat pengguna lain
        other_user = User.objects.create_user(username='otheruser', password='otherpass')
        self.client.logout()
        self.client.login(username='otheruser', password='otherpass')
        
        response = self.client.post(reverse('discuss_forum:edit_forum', args=[self.discussion.id]), {
            'title': 'Tidak Boleh Edit',
            'content': 'Tidak boleh edit diskusi orang lain.'
        })
        self.assertEqual(response.status_code, 403)
        self.discussion.refresh_from_db()
        self.assertNotEqual(self.discussion.title, 'Tidak Boleh Edit')
    
    def test_permission_delete_comment(self):
        # Membuat pengguna lain
        other_user = User.objects.create_user(username='otheruser', password='otherpass')
        self.client.logout()
        self.client.login(username='otheruser', password='otherpass')
        
        response = self.client.post(reverse('discuss_forum:delete_comment', args=[self.comment.id]))
        self.assertEqual(response.status_code, 403)
        self.assertTrue(Comment.objects.filter(id=self.comment.id).exists())
    
    def test_total_likes_property(self):
        self.assertEqual(self.comment.total_likes, 0)
        self.comment.likes.add(self.user)
        self.assertEqual(self.comment.total_likes, 1)

# ============================
# Tests untuk Models (Jika Diperlukan)
# ============================

class ModelsTests(TestCase):
    def test_moodentry_str_representation(self):
        now = timezone.now()
        mood = MoodEntry.objects.create(
            mood="Test Mood",
            time=now,
            feelings="Feeling test",
            mood_intensity=5,
        )
        self.assertEqual(str(mood), "Test Mood")

    def test_discussion_str_representation(self):
        user = User.objects.create_user(username='testuser', password='testpass')
        discussion = Discussion.objects.create(
            user=user,
            title="Test Discussion",
            content="Test content."
        )
        self.assertEqual(str(discussion), "Test Discussion")
    
    def test_comment_str_representation(self):
        user = User.objects.create_user(username='testuser', password='testpass')
        discussion = Discussion.objects.create(
            user=user,
            title="Test Discussion",
            content="Test content."
        )
        comment = Comment.objects.create(
            discussion=discussion,
            user=user,
            content="Test Comment"
        )
        expected_str = f"Komentar oleh {user.username} pada {discussion.title}"
        self.assertEqual(str(comment), expected_str)
    
    def test_comment_total_likes(self):
        user = User.objects.create_user(username='testuser', password='testpass')
        comment = Comment.objects.create(
            discussion=Discussion.objects.create(
                user=user,
                title="Test Discussion",
                content="Test content."
            ),
            user=user,
            content="Test Comment"
        )
        self.assertEqual(comment.total_likes, 0)
        comment.likes.add(user)
        self.assertEqual(comment.total_likes, 1)

