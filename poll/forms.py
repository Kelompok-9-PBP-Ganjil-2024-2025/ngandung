from django.forms import ModelForm
from django import forms
from .models import Poll, Choice
from django.forms import inlineformset_factory, BaseFormSet
from django.forms.widgets import HiddenInput 

class PollForm(ModelForm):
    class Meta:
        model = Poll
        fields = ['question']
        
class BaseChoiceFormSet(BaseFormSet):
    def get_deletion_widget(self):
        return HiddenInput(attrs={"class": "deletion"})
    
ChoiceFormSet = inlineformset_factory(
    Poll, 
    Choice,
    formset=BaseChoiceFormSet,
    fields=['choice_text'], 
    extra=2,
    max_num=5,
    can_delete=True
)