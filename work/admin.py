from django.contrib import admin
from .models import HomeWorkInfModel, HomeWorkMembersModel


# Register your models here.

class HomeWorkAdmin(admin.ModelAdmin):
    list_display = ['name', 'owner_name']
    def owner_name(self,obj):
        return obj.owner.first_name
    owner_name.short_description = "创建人"
    list_display_links = ['name', 'owner_name']
    search_fields = ['name']
    readonly_fields = ['create_time']
    list_filter = ['owner', 'subject']


class HomeWorkMembersAdmin(admin.ModelAdmin):
    def owner_name(self,obj):
        return obj.owner.first_name
    owner_name.short_description = "完成人"
    list_display = ['work','owner_name','done']
    list_display_links =['work','owner_name']
    search_fields = ['work__name']


admin.site.register(HomeWorkInfModel, HomeWorkAdmin)
admin.site.register(HomeWorkMembersModel, HomeWorkMembersAdmin)
