from django.forms import ModelForm
from discuss_forum.models import Discussion
from discuss_forum.models import Comment

class DiscussionForm(ModelForm):
    class Meta:
        model = Discussion
        fields = ["title", "content"]

class DiscussionForumForm(ModelForm):
    class Meta:
        model = Comment
        fields = ["content"]