# urls.py
from django.urls import path
from discuss_forum import views

app_name = "discuss_forum"

urlpatterns = [
    path('forum/', views.forum_main, name='forum_main'),
    path('create-discussion-forum', views.create_discussion_forum, name='create_discussion_forum'),
    path('json/', views.show_json, name='show_json'),
    path('json/<str:id>/', views.show_json_by_id, name='show_json_by_id'),

    path('discussion/<uuid:id>/', views.discussion_main, name='discussion_main'),
    path('discussion/<uuid:id>/add-comment/', views.add_comment, name='add_comment'),

    path('create-forum-topic-ajax', views.add_forum_topic_ajax, name='add_forum_topic_ajax'),
    path('edit-forum/<uuid:id>', views.edit_forum, name='edit_forum'),
    path('delete/<uuid:id>', views.delete_forum, name='delete_forum'),

    path('edit-comment/<uuid:id>/', views.edit_comment, name='edit_comment'),
    path('delete-comment/<uuid:id>', views.delete_comment, name='delete_comment'),
    path('comment/<uuid:comment_id>/like/', views.like_comment, name='like_comment'),
    path('edit-forum-ajax/<uuid:id>/', views.edit_forum_ajax, name='edit_forum_ajax'),

    path('edit-comment-ajax/<uuid:id>/', views.edit_comment_ajax, name='edit_comment_ajax'),

    # API endpoints - Path spesifik terlebih dahulu
    path('api/current-user/', views.api_current_user, name='api_current_user'),
    path('api/forum', views.api_forum_main, name='api_forum_main'),
    path('api/<str:id>/', views.api_forum_by_id, name='api_forum_by_id'),
    path('create-forum-flutter/', views.api_create_forum_flutter, name='api_create_forum_flutter'),
    path('edit-forum-flutter/<uuid:id>/', views.api_edit_forum_flutter, name='api_edit_forum_flutter'),
    path('delete-forum-flutter/<uuid:id>/', views.api_delete_forum_flutter, name='api_delete_forum_flutter'),

    path('api/discussion/<uuid:id>/comments/', views.api_discussion_comments_by_forum_id, name='api_discussion_comments_by_forum_id'),
    path('api/discussion/<uuid:discussion_id>/add_comment/', views.api_create_comment_flutter, name='api_create_comment_flutter'),
    path('api/discussion/comments/<uuid:comment_id>/delete/', views.api_delete_comment_flutter, name='api_delete_comment_flutter'),
    path(
        'api/discussion/comments/<uuid:comment_id>/like/', 
        views.api_like_comment_flutter, 
        name='api_like_comment_flutter'
    ),]
