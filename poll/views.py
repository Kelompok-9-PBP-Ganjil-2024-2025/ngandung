from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render, redirect
from .forms import PollForm, VoteForm, ChoiceFormSet
from .models import Choice, Poll, Vote
from django.db.models import Case, When, IntegerField
from django.http import JsonResponse
from django.urls import reverse
from django.http import HttpResponseRedirect, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.core import serializers
import json

@csrf_exempt
@login_required
def polls(request):
    data = Poll.objects.select_related('author').all()
    serialized_data = [
        {
            "id": poll.id,
            "author": poll.author.username,
            "question": poll.question,
            "is_active": poll.is_active,
            "view_results": poll.author == request.user or not poll.is_active or Vote.objects.filter(poll=poll, user=request.user).exists()
        }
        for poll in data
    ]
    return JsonResponse(serialized_data, safe=False)

@csrf_exempt
@login_required 
def create(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)

            # Extract poll data
            question = data.get('question', '')
            is_active = data.get('is_active', 'true').lower() == 'true'
            choices = data.get('choices', [])

            # Validate poll data
            if not question or not choices:
                return JsonResponse({'error': 'Invalid data: Missing question or choices'}, status=400)

            # Create the poll
            poll = Poll.objects.create(
                question=question,
                is_active=is_active,
                author=request.user  # Use the authenticated user
            )

            # Create choices
            for choice_data in choices:
                choice_text = choice_data.get('choice_text', '')
                if choice_text:
                    Choice.objects.create(poll=poll, choice_text=choice_text)

            return JsonResponse({'message': 'Poll created successfully!', 'status': 200}, status=200)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON format'}, status=400)
        except Exception as e:
            return JsonResponse({'error': f'An error occurred: {str(e)}'}, status=500)
    else:
        return JsonResponse({'error': 'Only POST requests are allowed'}, status=405)

@csrf_exempt
@login_required
def update(request, poll_id):
    try:
        poll = Poll.objects.get(pk=poll_id)
        poll.is_active = not poll.is_active  # Toggle the is_active field
        poll.save()

        return JsonResponse({'status': 'success'})
    except Poll.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Poll not found'})


@csrf_exempt
@login_required
def vote(request, poll_id):
    poll = get_object_or_404(Poll, pk=poll_id)
    vote = Vote.objects.filter(poll=poll, user=request.user).first()
    if vote:
        return JsonResponse({'status': 'error', 'message': 'You have already voted.'}, status=400)
    if poll.author == request.user:
        return JsonResponse({'status': 'error', 'message': 'Poll author cannot vote.'}, status=400)
    if not poll.is_active:
        return JsonResponse({'status': 'error', 'message': 'Poll is not active.'}, status=400)

    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            choice_id = data.get('choice')
            if not choice_id:
                return JsonResponse({'status': 'error', 'message': 'Choice is required.'}, status=400)

            choice = get_object_or_404(Choice, pk=choice_id, poll=poll)
            choice.vote_count += 1
            choice.save()
            Vote.objects.create(poll=poll, choice=choice, user=request.user)

            return JsonResponse({'status': 'success', 'message': 'Vote recorded successfully.'})
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON data.'}, status=400)
    elif request.method == 'GET':
        # Corrected 'text' to 'choice_text' based on the model field name.
        choices = list(poll.choices.values('id', 'choice_text', 'vote_count'))
        return JsonResponse({'poll': poll.question, 'choices': choices, 'status': 'success'})
    
    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'}, status=405)

@csrf_exempt
@login_required
def delete(request, poll_id):
    if request.method == "POST":  # Ensure the request method is POST
        poll = get_object_or_404(Poll, pk=poll_id)
        if request.user.is_superuser or request.user == poll.author:
            poll.delete()
            return JsonResponse({'status': 'success'})
        else:
            return JsonResponse({'status': 'error', 'message': 'You are not authorized to delete this poll'}, status=403)
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)   

@csrf_exempt
@login_required
def ajax_poll_results(request, poll_id):
    poll = get_object_or_404(Poll, pk=poll_id)
    choices = Choice.objects.filter(poll=poll)
    vote = Vote.objects.filter(poll=poll, user=request.user).first()

    if not vote and poll.author != request.user and poll.is_active:
        return JsonResponse({'error': 'You need to vote before viewing the results.'}, status=403)

    choices_data = [{'choice_text': choice.choice_text, 'vote_count': choice.vote_count} for choice in choices]
    data = {
        'status': 'success',
        'author': poll.author.username,
        'poll': poll.question,
        'choices': choices_data
    }
    return JsonResponse(data)