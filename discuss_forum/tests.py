# discuss_forum/tests.py

from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Discussion, Comment
import uuid


class DiscussionModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="password")
        self.discussion = Discussion.objects.create(
            user=self.user,
            title="Test Discussion",
            content="This is a test discussion.",
        )

    def test_discussion_creation(self):
        self.assertEqual(self.discussion.title, "Test Discussion")
        self.assertEqual(self.discussion.content, "This is a test discussion.")
        self.assertIsInstance(self.discussion.id, uuid.UUID)
        self.assertEqual(str(self.discussion), "Test Discussion")

    def test_discussion_str_method(self):
        self.assertEqual(str(self.discussion), self.discussion.title)


class CommentModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="commentuser", password="password"
        )
        self.discussion = Discussion.objects.create(
            user=self.user,
            title="Discussion for Comment",
            content="Content of the discussion.",
        )
        self.comment = Comment.objects.create(
            discussion=self.discussion,
            user=self.user,
            content="This is a test comment.",
        )

    def test_comment_creation(self):
        self.assertEqual(self.comment.content, "This is a test comment.")
        self.assertIsInstance(self.comment.id, uuid.UUID)
        self.assertEqual(
            str(self.comment),
            f"Komentar oleh {self.user.username} pada {self.discussion.title}",
        )

    def test_total_likes_property(self):
        # Initially, there should be no likes
        self.assertEqual(self.comment.total_likes, 0)
        # Add a like
        self.comment.likes.add(self.user)
        self.assertEqual(self.comment.total_likes, 1)


class ForumViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="viewuser", password="password")
        self.discussion = Discussion.objects.create(
            user=self.user,
            title="View Test Discussion",
            content="Content for view test.",
        )
        self.comment = Comment.objects.create(
            discussion=self.discussion, user=self.user, content="View test comment."
        )

    def test_create_discussion_forum_view_authenticated(self):
        self.client.login(username="viewuser", password="password")
        response = self.client.post(
            reverse("discuss_forum:create_discussion_forum"),
            {"title": "New Discussion", "content": "Content of the new discussion."},
        )
        self.assertEqual(response.status_code, 302)  # Redirect after creation
        self.assertTrue(Discussion.objects.filter(title="New Discussion").exists())

    def test_create_discussion_forum_view_unauthenticated(self):
        response = self.client.post(
            reverse("discuss_forum:create_discussion_forum"),
            {"title": "Should Not Create", "content": "No content."},
        )
        self.assertEqual(response.status_code, 302)  # Redirect to login
        self.assertFalse(Discussion.objects.filter(title="Should Not Create").exists())

    def test_add_comment_view_authenticated(self):
        self.client.login(username="viewuser", password="password")
        response = self.client.post(
            reverse("discuss_forum:add_comment", args=[self.discussion.id]),
            {"content": "Another test comment."},
        )
        self.assertEqual(response.status_code, 302)  # Redirect after adding comment
        self.assertTrue(
            Comment.objects.filter(content="Another test comment.").exists()
        )

    def test_add_comment_view_unauthenticated(self):
        response = self.client.post(
            reverse("discuss_forum:add_comment", args=[self.discussion.id]),
            {"content": "Should not be added."},
        )
        self.assertEqual(response.status_code, 302)  # Redirect to login
        self.assertFalse(
            Comment.objects.filter(content="Should not be added.").exists()
        )

    def test_like_comment_authenticated(self):
        self.client.login(username="viewuser", password="password")
        response = self.client.post(
            reverse("discuss_forum:like_comment", args=[self.comment.id]),
            HTTP_X_REQUESTED_WITH="XMLHttpRequest",
        )
        self.assertEqual(response.status_code, 200)
        self.comment.refresh_from_db()
        self.assertIn(self.user, self.comment.likes.all())

        # Unlike the comment
        response = self.client.post(
            reverse("discuss_forum:like_comment", args=[self.comment.id]),
            HTTP_X_REQUESTED_WITH="XMLHttpRequest",
        )
        self.assertEqual(response.status_code, 200)
        self.comment.refresh_from_db()
        self.assertNotIn(self.user, self.comment.likes.all())

    def test_like_comment_unauthenticated(self):
        response = self.client.post(
            reverse("discuss_forum:like_comment", args=[self.comment.id]),
            HTTP_X_REQUESTED_WITH="XMLHttpRequest",
        )
        self.assertEqual(response.status_code, 302)  # Redirect to login


class PermissionTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.owner = User.objects.create_user(username="owner", password="password")
        self.other_user = User.objects.create_user(
            username="other", password="password"
        )
        self.discussion = Discussion.objects.create(
            user=self.owner, title="Owner Discussion", content="Owned by owner."
        )
        self.comment = Comment.objects.create(
            discussion=self.discussion, user=self.owner, content="Owner comment."
        )

    def test_edit_discussion_by_owner(self):
        self.client.login(username="owner", password="password")
        response = self.client.post(
            reverse("discuss_forum:edit_forum", args=[self.discussion.id]),
            {"title": "Edited Title", "content": "Edited content."},
        )
        self.assertEqual(response.status_code, 302)
        self.discussion.refresh_from_db()
        self.assertEqual(self.discussion.title, "Edited Title")

    def test_edit_discussion_by_other_user(self):
        self.client.login(username="other", password="password")
        response = self.client.post(
            reverse("discuss_forum:edit_forum", args=[self.discussion.id]),
            {"title": "Hacked Title", "content": "Hacked content."},
        )
        self.assertEqual(response.status_code, 403)
        self.discussion.refresh_from_db()
        self.assertNotEqual(self.discussion.title, "Hacked Title")

    def test_delete_discussion_by_owner(self):
        self.client.login(username="owner", password="password")
        response = self.client.post(
            reverse("discuss_forum:delete_forum", args=[self.discussion.id])
        )
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Discussion.objects.filter(id=self.discussion.id).exists())

    def test_delete_discussion_by_other_user(self):
        self.client.login(username="other", password="password")
        response = self.client.post(
            reverse("discuss_forum:delete_forum", args=[self.discussion.id])
        )
        self.assertEqual(response.status_code, 403)
        self.assertTrue(Discussion.objects.filter(id=self.discussion.id).exists())

    def test_edit_comment_by_owner(self):
        self.client.login(username="owner", password="password")
        response = self.client.post(
            reverse("discuss_forum:edit_comment", args=[self.comment.id]),
            {"content": "Edited comment."},
        )
        self.assertEqual(response.status_code, 302)
        self.comment.refresh_from_db()
        self.assertEqual(self.comment.content, "Edited comment.")

    def test_edit_comment_by_other_user(self):
        self.client.login(username="other", password="password")
        response = self.client.post(
            reverse("discuss_forum:edit_comment", args=[self.comment.id]),
            {"content": "Hacked comment."},
        )
        self.assertEqual(response.status_code, 403)
        self.comment.refresh_from_db()
        self.assertNotEqual(self.comment.content, "Hacked comment.")

    def test_delete_comment_by_owner(self):
        self.client.login(username="owner", password="password")
        response = self.client.post(
            reverse("discuss_forum:delete_comment", args=[self.comment.id])
        )
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Comment.objects.filter(id=self.comment.id).exists())

    def test_delete_comment_by_other_user(self):
        self.client.login(username="other", password="password")
        response = self.client.post(
            reverse("discuss_forum:delete_comment", args=[self.comment.id])
        )
        self.assertEqual(response.status_code, 403)
        self.assertTrue(Comment.objects.filter(id=self.comment.id).exists())
