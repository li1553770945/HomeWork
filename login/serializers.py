from rest_framework import serializers
import re
from django.contrib.auth.models import User


class LoginSerializer(serializers.Serializer):  # 用于登录的表单合法性验证，防止绕过前端验证
    username = serializers.CharField()
    password = serializers.CharField()
    remember = serializers.BooleanField()

    def validate_username(self, username):
        if re.match("^[a-zA-Z0-9]{5,15}$", username) is None:
            raise serializers.ValidationError("用户名不符合规定")
        else:
            return username

    def validate_password(self, password):
        if len(password) != 32:
            raise serializers.ValidationError("密码长度不正确")
        else:
            return password

class RegisterSerializer(serializers.Serializer):  # 用于注册的表单合法性验证，防止绕过前端验证
    username = serializers.CharField()
    password = serializers.CharField()
    nickname = serializers.CharField()

    def validate_username(self, username):
        if re.match('^[a-zA-Z0-9]{5,15}$', username) is None:
            raise serializers.ValidationError("学号不符合规定")
        else:
            return username

    def validate_password(self, password):
        if len(password) != 32:
            raise serializers.ValidationError("密码长度不正确")
        else:
            return password

    def validate_nickname(self, nickname):
        if re.match("^[\u4e00-\u9fa5·]{2,18}$", nickname) is None:
            raise serializers.ValidationError("姓名不符合规定")
        else:
            return nickname

class UserSerializer(serializers.ModelSerializer): # 用于获取用户信息，反馈给用户
    name = serializers.SerializerMethodField()
    def get_name(self, obj):
        return obj.first_name

    class Meta:
        model = User
        fields = ['id','last_login', 'username','name', 'date_joined']