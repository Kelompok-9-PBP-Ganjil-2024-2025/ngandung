from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from .models import Poll, Choice, Vote
from .forms import PollForm, VoteForm, ChoiceFormSet
import uuid

class ModelTests(TestCase):
    def setUp(self):
        # Create test user
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        
        # Create test poll
        self.poll = Poll.objects.create(
            author=self.user,
            question="Test question?",
            is_active=True
        )
        
        # Create choices for the poll
        self.choice1 = Choice.objects.create(
            poll=self.poll,
            choice_text="Choice 1"
        )
        self.choice2 = Choice.objects.create(
            poll=self.poll,
            choice_text="Choice 2"
        )

    def test_poll_creation(self):
        self.assertIsInstance(self.poll.id, uuid.UUID)
        self.assertEqual(str(self.poll), "Test question?")
        self.assertEqual(self.poll.author, self.user)
        self.assertTrue(self.poll.is_active)

    def test_choice_creation(self):
        self.assertIsInstance(self.choice1.id, uuid.UUID)
        self.assertEqual(str(self.choice1), "Choice 1")
        self.assertEqual(self.choice1.vote_count, 0)
        self.assertEqual(self.choice1.poll, self.poll)

    def test_vote_creation(self):
        vote = Vote.objects.create(
            poll=self.poll,
            choice=self.choice1,
            user=self.user
        )
        self.assertIsInstance(vote.id, uuid.UUID)
        expected_str = f'{self.user.username} voted for {self.choice1.choice_text}'
        self.assertEqual(str(vote), expected_str)

    def test_vote_unique_constraint(self):
        Vote.objects.create(
            poll=self.poll,
            choice=self.choice1,
            user=self.user
        )
        # Try to create another vote for the same user and poll
        with self.assertRaises(Exception):
            Vote.objects.create(
                poll=self.poll,
                choice=self.choice2,
                user=self.user
            )

class ViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        # Create two users
        self.user1 = User.objects.create_user(
            username='testuser1',
            password='testpass123'
        )
        self.user2 = User.objects.create_user(
            username='testuser2',
            password='testpass123'
        )
        
        # Create a test poll
        self.poll = Poll.objects.create(
            author=self.user1,
            question="Test question?",
            is_active=True
        )
        
        # Create choices
        self.choice1 = Choice.objects.create(
            poll=self.poll,
            choice_text="Choice 1"
        )
        self.choice2 = Choice.objects.create(
            poll=self.poll,
            choice_text="Choice 2"
        )

    def test_home_view_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('poll:home'))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith('/login'))

    def test_home_view_logged_in(self):
        self.client.login(username='testuser1', password='testpass123')
        response = self.client.get(reverse('poll:home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'poll_list.html')
        self.assertTrue('my_polls' in response.context)
        self.assertTrue('other_polls' in response.context)

    def test_create_poll(self):
        self.client.login(username='testuser1', password='testpass123')
        poll_data = {
            'question': 'New test question?',
            'is_active': True,
            'form-TOTAL_FORMS': '2',
            'form-INITIAL_FORMS': '0',
            'form-MIN_NUM_FORMS': '0',
            'form-MAX_NUM_FORMS': '5',
            'form-0-choice_text': 'New Choice 1',
            'form-1-choice_text': 'New Choice 2',
        }
        response = self.client.post(reverse('poll:create'), poll_data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Poll.objects.filter(question='New test question?').exists())

    def test_vote_view(self):
        self.client.login(username='testuser2', password='testpass123')
        vote_data = {
            'choice': self.choice1.id
        }
        response = self.client.post(
            reverse('poll:vote', kwargs={'poll_id': self.poll.id}),
            vote_data
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Vote.objects.filter(
            user=self.user2,
            poll=self.poll,
            choice=self.choice1
        ).exists())
        
    def test_ajax_poll_results(self):
        self.client.login(username='testuser2', password='testpass123')
        # Create a vote first
        Vote.objects.create(
            poll=self.poll,
            choice=self.choice1,
            user=self.user2
        )
        response = self.client.get(
            reverse('poll:ajax_poll_results', kwargs={'poll_id': self.poll.id})
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['poll'], 'Test question?')
        self.assertEqual(len(data['choices']), 2)

    def test_update_poll(self):
        self.client.login(username='testuser1', password='testpass123')
        update_data = {
            'question': 'Updated question?',
            'is_active': False
        }
        response = self.client.post(
            reverse('poll:update', kwargs={'poll_id': self.poll.id}),
            update_data
        )
        self.assertEqual(response.status_code, 302)
        updated_poll = Poll.objects.get(id=self.poll.id)
        self.assertEqual(updated_poll.question, 'Updated question?')
        self.assertFalse(updated_poll.is_active)

    def test_delete_poll(self):
        self.client.login(username='testuser1', password='testpass123')
        response = self.client.post(
            reverse('poll:delete', kwargs={'poll_id': self.poll.id})
        )
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Poll.objects.filter(id=self.poll.id).exists())

class FormTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.poll = Poll.objects.create(
            author=self.user,
            question="Test question?",
            is_active=True
        )
        self.choice = Choice.objects.create(
            poll=self.poll,
            choice_text="Choice 1"
        )

    def test_poll_form_valid(self):
        form_data = {
            'question': 'Test question?',
            'is_active': True
        }
        form = PollForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_poll_form_invalid(self):
        form_data = {
            'question': '',  # Empty question should be invalid
            'is_active': True
        }
        form = PollForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_vote_form(self):
        form = VoteForm(poll=self.poll)
        self.assertEqual(
            list(form.fields['choice'].queryset),
            list(Choice.objects.filter(poll=self.poll))
        )

    def test_choice_formset(self):
        formset_data = {
            'form-TOTAL_FORMS': '2',
            'form-INITIAL_FORMS': '0',
            'form-MIN_NUM_FORMS': '0',
            'form-MAX_NUM_FORMS': '5',
            'form-0-choice_text': 'Choice 1',
            'form-1-choice_text': 'Choice 2',
        }
        formset = ChoiceFormSet(data=formset_data)
        self.assertTrue(formset.is_valid())