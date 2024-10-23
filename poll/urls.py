from .views import *
from django.urls import path

urlpatterns = [
    path('', poll_list, name='home'),
    path('create/', create, name='create'),
    path('vote/<uuid:poll_id>/', vote, name='vote'),
    path('results/<uuid:poll_id>/', results, name='results'),
]