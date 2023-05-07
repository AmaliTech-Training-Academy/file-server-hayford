from django.contrib import admin
from .models import FileModels

# Register your models here.
class FileAdmin(admin.ModelAdmin):
    list_display = ('title', 'downloads', 'emails_sent')



class CustomUserAdmin(admin.ModelAdmin):
    pass 



admin.site.register(FileModels, FileAdmin)