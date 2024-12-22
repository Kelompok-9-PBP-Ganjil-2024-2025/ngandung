# discuss_forum/serializers.py
from rest_framework import serializers
from .models import Discussion, Comment
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']

class CommentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    replies = serializers.SerializerMethodField()
    likes = UserSerializer(many=True, read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'discussion', 'user', 'content', 'parent', 'date_created', 'likes', 'replies']

    def get_replies(self, obj):
        # Mendapatkan balasan (replies) dari komentar
        if obj.replies.exists():
            return CommentSerializer(obj.replies.all(), many=True).data
        return []

class DiscussionSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    comments = serializers.SerializerMethodField()

    class Meta:
        model = Discussion
        fields = ['id', 'user', 'title', 'content', 'date_created', 'last_updated', 'comments']

    def get_comments(self, obj):
        # Mendapatkan komentar tingkat atas (tanpa parent)
        top_comments = obj.comments.filter(parent__isnull=True).order_by('-date_created')
        return CommentSerializer(top_comments, many=True).data
