from django.contrib import admin
from django.urls import path, include, re_path
from django.views.generic.base import RedirectView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("toko_makanan.urls")),
    # To handle any URL that doesn't match the ones above
    re_path(r"^.*$", RedirectView.as_view(url="/", permanent=False)),
]
