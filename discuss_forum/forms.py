from django.forms import ModelForm
from discuss_forum.models import Discussion

class DiscussionForm(ModelForm):
    class Meta:
        model = Discussion
        fields = ["title", "content"]