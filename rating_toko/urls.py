from django.urls import path
from rating_toko.views import get_all_toko_page, get_all_toko, get_all_ratings_page, get_all_ratings, add_rating, edit_rating, delete_rating, get_toko, get_user

app_name = "rating_toko"

urlpatterns = [
    # Toko page
    path("rating-toko/", get_all_toko_page, name="get_all_toko_page"),
    path("api/toko/", get_all_toko, name="get_all_toko"),
    path("api/toko/<int:id_rumah_makan>/", get_toko, name="get_toko"),
    # Specific toko page
    path("rating-toko/<int:id_rumah_makan>/", get_all_ratings_page, name="get_all_ratings_page"),
    path("api/rating-toko/<int:id_rumah_makan>/", get_all_ratings, name="get_all_ratings"),
    path("api/rating-toko/add/", add_rating, name="add_rating"),
    path("api/rating-toko/edit/<int:id_rating>/<int:id_rumah_makan>/", edit_rating, name="edit_rating"),
    path("api/rating-toko/delete/", delete_rating, name="delete_rating"),
    # User
    path("api/user/<int:id_user>/", get_user, name="get_user"),
]