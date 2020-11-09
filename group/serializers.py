from rest_framework import serializers
from .models import GroupModel
import re


class GroupSerializer(serializers.ModelSerializer):
    members = serializers.SerializerMethodField()

    class Meta:
        model = GroupModel
        fields = ['id', 'name', 'desc', 'create_time', 'owner', 'members', 'password']

    def get_members(self, obj):
        members_list=list()
        members=obj.get_members()
        for member in members:
            members_list.append({'id':member.id,'name':member.first_name})
        return members_list


class GroupUnSerializer(serializers.Serializer):
    name = serializers.CharField()
    desc = serializers.CharField()
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
        return re.match("^[a-zA-Z0-9\u4e00-\u9fa5_丶]{5,200}$", data) is not None
    if name == 'password':
        return re.match("^(?![0-9]+$)(?![a-zA-Z]+$)[0-9A-Za-z\\W]{6,18}$", data) is not None


class GroupsSerializer(serializers.Serializer):
    id = serializers.SerializerMethodField()
    time = serializers.DateTimeField()
    name = serializers.SerializerMethodField()

    def get_id(self, obj):
        return obj.group.id

    def get_name(self, obj):
        return obj.group.name


class CreateGroupsSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    time = serializers.SerializerMethodField()
    name = serializers.CharField()

    def get_time(self, obj):
        return obj.create_time
