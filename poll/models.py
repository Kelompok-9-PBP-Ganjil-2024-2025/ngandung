from django.db import models
import uuid
from django.contrib.auth.models import User
from main.models import Makanan

# Create your models here.
class Poll(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.CharField(max_length=200)
    is_active = models.BooleanField(default=True)
        
    def __str__(self):
        return self.question
    
class Choice(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE, related_name='choices')
    choice_text = models.CharField(max_length=200)
    vote_count = models.IntegerField(default=0)
        
    def __str__(self):
        return self.choice_text
    
class Vote(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE, related_name='votes')
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE, related_name='votes')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    class Meta:
        unique_together = ('poll', 'user')
        
    def __str__(self):
        return f'{self.user.username} voted for {self.choice.choice_text}'