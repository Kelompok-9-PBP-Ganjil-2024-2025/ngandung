from django.urls import path
from rating_toko.views import show_rating

app_name = "rating_toko"

urlpatterns = [
    path("rating/<str:id_toko>/", show_rating, name="show_rating"),
    path("rating/", show_rating, name="show_rating"),
]