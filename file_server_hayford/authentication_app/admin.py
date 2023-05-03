from django.contrib import admin
from django.contrib import admin
from .models import signUser
# Register your models here.

admin.site.register(signUser)

class CustomUserAdmin(admin.ModelAdmin):
    pass