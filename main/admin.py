# Register your models here.
from django.contrib import admin
from .models import UserProfile, Toko, Makanan

# Register the models so they are accessible in the admin interface
admin.site.register(UserProfile)
admin.site.register(Toko)
admin.site.register(Makanan)
