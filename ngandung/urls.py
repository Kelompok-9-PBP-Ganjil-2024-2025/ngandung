from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("main.urls")),
    path("", include("toko_makanan.urls")),
    path("", include("authentication.urls")),
    path("", include("rating_toko.urls")),
]
