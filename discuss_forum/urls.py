# urls.py
from django.urls import path
from discuss_forum.views import (
    api_create_comment_flutter,
    api_create_forum_flutter,
    api_current_user,
    api_delete_forum_flutter,
    api_discussion_comments_by_forum_id,
    api_edit_forum_flutter,
    api_forum_by_id,
    api_forum_main,
    delete_forum_flutter,
    forum_main, 
    add_forum_topic_ajax, 
    create_discussion_forum, 
    show_json, 
    show_json_by_id, 
    discussion_main,
    add_comment,
    edit_forum,
    delete_forum,
    edit_comment,
    delete_comment,
    edit_forum_ajax,
    edit_comment_ajax
)
from django.conf import settings
from django.conf.urls.static import static

from . import views

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

    path('edit-comment/<uuid:id>/', edit_comment, name='edit_comment'),
    path('delete-comment/<uuid:id>', delete_comment, name='delete_comment'),
    path('comment/<uuid:comment_id>/like/', views.like_comment, name='like_comment'),
    path('edit-forum-ajax/<uuid:id>/', edit_forum_ajax, name='edit_forum_ajax'),

    path('edit-comment-ajax/<uuid:id>/', edit_comment_ajax, name='edit_comment_ajax'),


    path('api/forum', api_forum_main, name='api_forum_main'),
    path('api/<str:id>/', api_forum_by_id, name='api_forum_by_id'),
    path('create-forum-flutter/', api_create_forum_flutter, name='api_create_forum_flutter'),
    path('edit-forum-flutter/<uuid:id>/', api_edit_forum_flutter, name='api_create_forum_flutter'),
    path('delete-forum-flutter/<uuid:id>/', delete_forum_flutter, name='delete_forum_flutter'),
    path('api/current-user/', api_current_user, name='api_current_user'),




    path('api/discussion/<uuid:id>/comments/', api_discussion_comments_by_forum_id, name='api_discussion_comments_by_forum_id'),

    path('api/discussion/<uuid:discussion_id>/add_comment/', views.api_create_comment_flutter, name='api_create_comment_flutter'),
]
