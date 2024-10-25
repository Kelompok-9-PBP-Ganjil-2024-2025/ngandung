from django.urls import path
from discuss_forum.views import forum_main, add_forum_topic_ajax, create_discussion_forum, show_json, show_json_by_id

app_name = "discuss_forum"

urlpatterns = [
    path('forum/', forum_main, name='forum_main'),
    path('create-discussion-forum', create_discussion_forum, name='create_discussion_forum'),
    path('json/', show_json, name='show_json'),
    path('json/<str:id>/', show_json_by_id, name='show_json_by_id'),

    path('create-forum-topic-ajax', add_forum_topic_ajax, name='add_forum_topic_ajax'),
]