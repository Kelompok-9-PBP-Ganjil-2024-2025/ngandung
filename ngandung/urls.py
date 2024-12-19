from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    # path("polling-makanan/", include("poll.urls")),
    path("", include("main.urls")),
    path("", include("toko_makanan.urls")),
    path("", include("authentication.urls")),
    path("auth/", include("auth_flutter.urls")),
    path("", include("rating_toko.urls")),
    path("", include("dev_favorite_store.urls")),
    path("", include("discuss_forum.urls")),
    path("polling-makanan/", include("poll.urls")),
]