from django.contrib import admin
from .models import GroupModel, GroupMembersModel, WorkGroupModel


# Register your models here.
class GroupAdmin(admin.ModelAdmin):
    list_display_links = ['name', 'owner']
    search_fields = ['owner__username']
    list_display = ['name', 'owner']


class GroupMembersAdmin(admin.ModelAdmin):
    list_display_links = ['group', 'user']
    search_fields = ['group__name', 'user__first_name']
    list_display = ['group', 'user']


class WorkGroupAdmin(admin.ModelAdmin):
    list_display_links = ['group', 'work']
    list_display = ['group', 'work']


admin.site.register(GroupModel, GroupAdmin)
admin.site.register(GroupMembersModel, GroupMembersAdmin)
admin.site.register(WorkGroupModel, WorkGroupAdmin)
