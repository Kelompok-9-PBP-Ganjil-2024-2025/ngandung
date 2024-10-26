from .views import *
from django.urls import path


app_name = 'poll'

urlpatterns = [
    path('', home, name='home'),
    path('create/', create, name='create'),
    path('update/<uuid:poll_id>/', update, name='update'),
    path('vote/<uuid:poll_id>/', vote, name='vote'),
    path('json/', pollsjson, name='polls-json'),
    path('delete/<uuid:poll_id>/', delete, name='delete'),
    path('ajax_poll_results/<uuid:poll_id>/', ajax_poll_results, name='ajax_poll_results'),
]