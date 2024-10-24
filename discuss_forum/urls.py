from django.urls import path
from discuss_forum.views import forum_main

app_name = "discuss_forum"

urlpatterns = [
    path('forum/', forum_main, name='forum_main'),
]