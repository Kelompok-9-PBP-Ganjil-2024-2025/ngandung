from django.urls import path
from auth_flutter.views import login_user
from auth_flutter.views import register
from auth_flutter.views import logout_user

app_name = "auth_flutter"

urlpatterns = [
    path('login/', login_user, name='login'),
    path('register/', register, name='register'),
    path('logout/', logout_user, name='logout'),
]