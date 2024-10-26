from django.forms import ModelForm
from discuss_forum.models import Discussion, Comment
from django import forms


class DiscussionForm(ModelForm):
    class Meta:
        model = Discussion
        fields = ["title", "content"]

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'rows': 4,
                'style': 'width: 100%;',
                'placeholder': 'Tambahkan komentar Anda...'
            })
        }