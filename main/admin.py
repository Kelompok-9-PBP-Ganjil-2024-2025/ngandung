# Register your models here.
from django.contrib import admin
from .models import RumahMakan, Makanan
from dev_favorite_store.models import UserProfile

# Register the models so they are accessible in the admin interface
admin.site.register(RumahMakan)
admin.site.register(Makanan)
admin.site.register(UserProfile)
