from django.contrib import admin
from .models import HomeWorkInfModel, HomeWorkMembersModel


# Register your models here.

class HomeWorkAdmin(admin.ModelAdmin):
    list_display = ['name', 'owner']
    list_display_links = ['name', 'owner']
    search_fields = ['name']
    readonly_fields = ['create_time']
    list_filter = ['owner', 'subject']


class HomeWorkMembersAdmin(admin.ModelAdmin):
    list_display = ['work','owner','done']
    list_display_links =['work','owner']


admin.site.register(HomeWorkInfModel, HomeWorkAdmin)
admin.site.register(HomeWorkMembersModel, HomeWorkMembersAdmin)
