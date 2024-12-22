from .views import *
from django.urls import path


app_name = 'poll'

urlpatterns = [
    path('polls/', polls, name='polls'),
    path('create/', create, name='create'),
    path('update/<uuid:poll_id>/', update, name='update'),
    path('vote/<uuid:poll_id>/', vote, name='vote'),
    path('delete/<uuid:poll_id>/', delete, name='delete'),
    path('polls/<uuid:poll_id>/results/', ajax_poll_results, name='ajax_poll_results'),
]