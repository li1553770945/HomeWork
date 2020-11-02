from rest_framework import serializers
from .models import HomeWorkInfModel


class HomeWorkSerializer(serializers.Serializer):  # 用于登录的表单合法性验证，防止绕过前端验证
    name = serializers.CharField()
    type = serializers.CharField()
    subject = serializers.CharField()
    remark = serializers.CharField(required=False)
    end_time = serializers.CharField()
    member_can_know_donelist = serializers.CharField()
    member_can_see_others = serializers.CharField()

    def validate_name(self, name):
        if len(name) > 50:
            raise serializers.ValidationError("名称长度过长")
        return name

    def validate_type(self, type):
        types = ['file', 'hypertext']
        if type not in types:
            raise serializers.ValidationError("不支持的类型")
        return type

    def validate_subject(self, subject):
        if len(subject) > 30:
            raise serializers.ValidationError("科目过长")
        return subject

    def validate_remark(self, remark):
        if len(remark) > 500:
            raise serializers.ValidationError("备注过长")
        return remark

    def validate_end_time(self, end_time):
        try:
            int(end_time[0:4])
            int(end_time[5:7])
            int(end_time[8:10])
            int(end_time[11:13])
            int(end_time[14:16])
            return end_time
        except:
            raise serializers.ValidationError("日期格式不正确")


class HomeWorkInfSerializer(serializers.ModelSerializer):
    class Meta:
        model = HomeWorkInfModel
        fields = '__all__'
