from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    # path("polling-makanan/", include("poll.urls")),
    path("", include("main.urls")),
    path("", include("authentication.urls")),
    path('polling-makanan/', include('poll.urls')),
]
