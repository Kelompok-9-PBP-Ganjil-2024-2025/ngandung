from django.shortcuts import render, redirect
from .forms import PollForm, ChoiceFormSet
from .models import Poll

# Create your views here.
def poll_list(request):
    context = {}
    return render(request, 'poll_list', context)

def create(request):
    if request.method == 'POST':
        formset = ChoiceFormSet(request.POST)
        if poll_form.is_valid() and formset.is_valid():
            poll = poll_form.save()
            choices = formset.save(commit=False)
            for choice in choices:
                if choice not in formset.deleted_objects:
                    choice.poll = poll
                    choice.save()
                else:
                    choice.delete()
            return redirect('poll_list')  # Redirect to a poll list or success page
    else:
        poll_form = PollForm()
        formset = ChoiceFormSet()

    return render(request, 'poll_form.html', {
        'poll_form': poll_form,
        'formset': formset,
    })

def vote(request, poll_id):
    context = {}
    return render(request, 'vote.html', context)

def results(request, poll_id): 
    context = {}
    return render(request, 'results.html', context)