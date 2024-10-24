from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("main.urls")),
    path('', include('authentication.urls')),
    path('', include('discuss_forum.urls')),
]
