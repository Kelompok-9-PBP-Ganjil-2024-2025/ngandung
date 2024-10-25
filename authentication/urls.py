from django.urls import path
from authentication.views import login_user
from authentication.views import register
from authentication.views import logout_user
app_name = "authentication"

urlpatterns = [
    path('login/', login_user, name='login'),
    path('register/', register, name='register'),
    path('logout/', logout_user, name='logout'),
]