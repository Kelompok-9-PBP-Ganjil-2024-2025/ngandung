from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render, redirect
from .forms import PollForm, VoteForm, ChoiceFormSet
from .models import Choice, Poll, Vote
from django.http import JsonResponse
from django.urls import reverse
from django.http import HttpResponseRedirect

# Create your views here.
@login_required(login_url='/login')
def home(request):
    my_polls = Poll.objects.filter(author=request.user)
    other_polls = Poll.objects.exclude(author=request.user)
    votes = Vote.objects.filter(user=request.user)
    votes = [vote.poll_id for vote in votes]
    return render(request, 'poll_list.html', {'my_polls': my_polls, 'other_polls': other_polls, 'votes': votes})

@login_required(login_url='/login')
def pollsjson(request):
    polls = Poll.objects.all()
    return JsonResponse(list(polls.values()), safe=False)

@login_required(login_url='/login')
def create(request):
    if request.method == 'POST':
        poll_form = PollForm(request.POST)
        formset = ChoiceFormSet(request.POST)
        if poll_form.is_valid() and formset.is_valid():
            poll = poll_form.save(commit=False)
            poll.author = request.user
            poll.save()
            
            for form in formset:
                choice = form.save(commit=False)
                choice.poll = poll
                choice.save()
            return redirect('poll:home')  # Redirect to a poll list or success page
    else:
        poll_form = PollForm()
        formset = ChoiceFormSet()

    return render(request, 'poll_form.html', {
        'poll_form': poll_form,
        'formset': formset,
    })
    
@login_required(login_url='/login')
def update(request, poll_id):
    poll = get_object_or_404(Poll, pk=poll_id)
    print(poll)
    form = PollForm(request.POST or None, instance=poll)
    if poll.author != request.user:
        return redirect('poll:home')
    if form.is_valid() and request.method == "POST":
        form.save()
        return HttpResponseRedirect(reverse('poll:home'))
    else:
        form = PollForm(instance=poll)
        return render(request, 'poll_form.html', {'poll_form': form})


@login_required(login_url='/login')
def vote(request, poll_id):
    poll = get_object_or_404(Poll, pk=poll_id)
    vote = Vote.objects.filter(poll=poll, user=request.user).first()
    if vote or poll.author == request.user or not poll.is_active:
        return redirect('poll:results', poll_id=poll_id)
    if request.method == 'POST':
        form = VoteForm(request.POST, poll=poll)
        if form.is_valid():
            choice = form.cleaned_data['choice']
            choice.vote_count += 1
            choice.save()
            Vote.objects.create(poll=poll, choice=choice, user=request.user)
            return redirect('poll:home')
    else:
        form = VoteForm(poll=poll)
    
    return render(request, 'vote_form.html', {'form': form, 'poll': poll})

@login_required(login_url='/login')
def results(request, poll_id): 
    poll = get_object_or_404(Poll, pk=poll_id)
    choices = Choice.objects.filter(poll=poll)
    vote = Vote.objects.filter(poll=poll, user=request.user).first()

    if not vote and poll.author != request.user and poll.is_active:
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'error': 'You need to vote before viewing the results.'}, status=403)
        else:
            return redirect('poll:vote', poll_id=poll_id)

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        choices_data = [{'choice_text': choice.choice_text, 'vote_count': choice.vote_count} for choice in choices]
        data = {
            'poll': poll.question,
            'choices': choices_data
        }
        return JsonResponse(data)

    return render(request, 'results.html', {'poll': poll, 'choices': choices})

@login_required(login_url='/login')
def delete(request, poll_id):
    poll = get_object_or_404(Poll, pk=poll_id)
    if request.user == poll.author:
        poll.delete()
    return redirect('poll:home')

@login_required(login_url='/login')
def ajax_poll_results(request, poll_id):
    poll = get_object_or_404(Poll, pk=poll_id)
    choices = Choice.objects.filter(poll=poll)
    vote = Vote.objects.filter(poll=poll, user=request.user).first()

    if not vote and poll.author != request.user and poll.is_active:
        return JsonResponse({'error': 'You need to vote before viewing the results.'}, status=403)

    choices_data = [{'choice_text': choice.choice_text, 'vote_count': choice.vote_count} for choice in choices]
    data = {
        'author': poll.author.username,
        'poll': poll.question,
        'choices': choices_data
    }
    return JsonResponse(data)