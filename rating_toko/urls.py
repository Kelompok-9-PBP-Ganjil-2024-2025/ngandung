from django.urls import path
from rating_toko.views import show_rating, show_rating_detail_json

app_name = "rating_toko"

urlpatterns = [
    path("rating/", show_rating, name="show_rating"),
    path("api/rating/<int:id>/", show_rating_detail_json, name="show_rating_detail_json"),
]