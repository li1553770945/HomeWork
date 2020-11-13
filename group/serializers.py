from rest_framework import serializers
from .models import GroupModel,GroupMembersModel
import re


class GroupSerializer(serializers.ModelSerializer):
    owner = serializers.SerializerMethodField()

    class Meta:
        model = GroupModel
        fields = ['id', 'name', 'desc', 'create_time', 'owner', 'members', 'password']

    def get_owner(self, obj):
        return obj.owner.first_name


class GroupUnSerializer(serializers.Serializer):
    name = serializers.CharField()
    desc = serializers.CharField(required=False, default="")
    password = serializers.CharField()

    def validate_name(self, name):
        if valid_group_information('name', name):
            return name
        else:
            raise serializers.ValidationError("组名格式不正确")

    def validate_desc(self, desc):
        if valid_group_information('desc', desc):
            return desc
        else:
            raise serializers.ValidationError("描述格式不正确")

    def validate_password(self, password):
        if valid_group_information('password', password):
            return password
        else:
            raise serializers.ValidationError("密码格式不正确")


def valid_group_information(name, data):
    if name == 'name':
        return re.match("^[a-zA-Z0-9\u4e00-\u9fa5_丶]{1,20}$", data) is not None
    if name == 'desc':
        return re.match("^[a-zA-Z0-9\u4e00-\u9fa5_丶]{0,200}$", data) is not None
    if name == 'password':
        return re.match("^[0-9a-zA-Z]{6,18}$", data) is not None


class GroupsSerializer(serializers.Serializer):
    id = serializers.SerializerMethodField()
    time = serializers.SerializerMethodField()
    name = serializers.SerializerMethodField()
    owner = serializers.SerializerMethodField()

    def get_id(self, obj):
        return obj.group.id

    def get_name(self, obj):
        return obj.group.name

    def get_time(self, obj):
        return obj.time

    def get_owner(self, obj):
        return obj.group.owner.first_name


class CreateGroupsSerializer(serializers.ModelSerializer):
    class Meta:
        model = GroupModel
        fields = ['id', 'name', 'create_time']


class GroupMembersSerializer(serializers.Serializer):
    members = serializers.SerializerMethodField()

    def get_members(self, obj):
        members_list = list()
        members = GroupMembersModel.objects.filter(group=obj).order_by('user__first_name')
        for member in members:
            members_list.append({'id': member.user.id, 'name': member.user.first_name,'username':member.user.username})
        return members_list
