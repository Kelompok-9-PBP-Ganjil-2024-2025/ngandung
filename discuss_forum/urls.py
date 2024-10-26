from django.urls import path
from discuss_forum.views import (
    forum_main, 
    add_forum_topic_ajax, 
    create_discussion_forum, 
    show_json, 
    show_json_by_id, 
    discussion_main,
    add_comment,
    edit_forum,
    delete_forum
)
app_name = "discuss_forum"

urlpatterns = [
    path('forum/', forum_main, name='forum_main'),
    path('create-discussion-forum', create_discussion_forum, name='create_discussion_forum'),
    path('json/', show_json, name='show_json'),
    path('json/<str:id>/', show_json_by_id, name='show_json_by_id'),

    path('discussion/<uuid:id>/', discussion_main, name='discussion_main'),
    path('discussion/<uuid:id>/add-comment/', add_comment, name='add_comment'),

    path('create-forum-topic-ajax', add_forum_topic_ajax, name='add_forum_topic_ajax'),
    path('edit-forum/<uuid:id>', edit_forum, name='edit_forum'),
    path('delete/<uuid:id>', delete_forum, name='delete_forum'),
]