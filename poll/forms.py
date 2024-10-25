from django.forms import ModelForm
from django import forms
from .models import Poll, Choice
from django.forms import inlineformset_factory, BaseFormSet
from django.forms.widgets import HiddenInput 

class PollForm(ModelForm):
    class Meta:
        model = Poll
        fields = ['question', 'is_active']
        
class VoteForm(forms.Form):
    choice = forms.ModelChoiceField(queryset=Choice.objects.none(), widget=forms.RadioSelect)
    
    def __init__(self, *args, **kwargs):
        poll = kwargs.pop('poll', None)
        super().__init__(*args, **kwargs)
        if poll:
            self.fields['choice'].queryset = Choice.objects.filter(poll=poll)
        
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