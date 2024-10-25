from django.urls import path
from main.views import show_main, show_rumah_makan_json_by_id

app_name = "main"

urlpatterns = [
    path("api/rumah-makan/<int:id>/", show_rumah_makan_json_by_id, name="show_rumah_makan_json_by_id"),
]
