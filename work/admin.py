from django.contrib import admin
from .models import HomeWorkInfModel


# Register your models here.

class HomeWorkAdmin(admin.ModelAdmin):
    list_display = ['name', 'owner']
    list_display_links = ['name', 'owner']
    search_fields = ['name']
    readonly_fields = ['create_time']
    list_filter = ['owner', 'subject']


admin.site.register(HomeWorkInfModel, HomeWorkAdmin)
