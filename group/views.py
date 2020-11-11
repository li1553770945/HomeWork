from rest_framework.views import APIView, Response
from .serializers import GroupSerializer, GroupsSerializer, CreateGroupsSerializer, GroupUnSerializer, \
    GroupMembersSerializer
from .models import GroupModel, GroupMembersModel
from common.common import get_first_error
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from django.http import QueryDict


class CsrfExemptSessionAuthentication(SessionAuthentication):

    def enforce_csrf(self, request):
        return


class GroupView(APIView):
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)

    def get(self, request):
        context = dict()
        context['err_code'] = 0
        data = request.GET
        user = request.user
        if user.is_anonymous:
            context['err_code'] = 1001
            context['error'] = "您还未登录"
            return Response(context)
        id = data.get('id')
        if id is None:
            context['err_code'] = 2001
            context['error'] = "请求参数不正确"
            return Response(context)
        try:
            id = int(id)
        except:
            context['err_code'] = 2002
            context['error'] = "参数格式不正确"
            return Response(context)
        query = GroupModel.objects.filter(id=id)
        if not query.exists():  # 请求数据不存在
            context['err_code'] = 4004
            context['error'] = "无法找到您要的数据"
            return Response(context)
        group = query.first()
        is_member = GroupMembersModel.objects.filter(user=user, group=group).exists()
        is_owner = (group.owner == user)
        if not is_member and not is_owner:
            context['err_code'] = 4003
            context['error'] = "您无权查看此内容"
            return Response(context)
        context['data'] = GroupSerializer(group).data
        if not is_owner:
            del context['data']['password']
        context['data']['is_owner'] = is_owner
        return Response(context)

    def post(self, request):
        context = dict()
        context['err_code'] = 0
        data = request.POST
        user = request.user
        if user.is_anonymous:
            context['err_code'] = 1001
            context['error'] = "您还未登录"
            return Response(context)
        data = GroupUnSerializer(data=data)
        if not data.is_valid():  # 验证有效性
            errors = data.errors
            key, value = get_first_error(errors)
            context['error'] = value[0]
            context['err_code'] = 2002
            return Response(context)
        data = data.data
        group = GroupModel.objects.create(owner=user, name=data['name'], desc=data['desc'], password=data['password'])
        context['data'] = dict()
        context['data']['id'] = group.id
        return Response(context)

    def put(self, request):
        context = dict()
        context['err_code'] = 0
        user = request.user
        put_data = QueryDict(request.body)
        if user.is_anonymous:
            context['err_code'] = 1001
            context['error'] = "您还未登录"
            return Response(context)
        data = GroupUnSerializer(data=put_data)
        if not data.is_valid():  # 验证有效性
            errors = data.errors
            key, value = get_first_error(errors)
            context['error'] = value[0]
            context['err_code'] = 2002
            return Response(context)
        data = data.data

        id = put_data.get('id')
        if id is None:
            context['error'] = "没有请求的id"
            context['err_code'] = 2002
            return Response(context)
        try:
            id = int(id)
        except:
            context['err_code'] = 2002
            context['error'] = "参数格式不正确"
            return Response(context)
        querys = GroupModel.objects.filter(id=id)
        if not querys.exists():  # 请求数据不存在
            context['err_code'] = 4004
            context['error'] = "无法找到您要的数据"
            return Response(context)
        query = querys.first()
        if user != query.owner:
            context['err_code'] = 4003
            context['error'] = "您无权执行此操作"
            return Response(context)
        querys.update(name=data['name'], desc=data['desc'], password=data['password'])
        return Response(context)

    def delete(self, request):
        context = dict()
        context['err_code'] = 0
        user = request.user
        if user.is_anonymous:
            context['err_code'] = 1001
            context['error'] = "您还未登录"
            return Response(context)
        data = QueryDict(request.body)
        id = data.get('id')
        if id is None:
            context['err_code'] = 2001
            context['error'] = "请求参数不正确"
            return Response(context)
        try:
            id = int(id)
        except:
            context['err_code'] = 2002
            context['error'] = "参数格式不正确"
            return Response(context)
        group = GroupModel.objects.filter(id=id)
        if not group.exists():
            context['err_code'] = 4004
            context['error'] = "该小组不存在"
            return Response(context)
        group = group.first()
        if user != group.owner:
            context['err_code'] = 4003
            context['error'] = "没有权限执行该操作"
            return Response(context)
        group.delete()
        return Response(context)


class GroupMembersView(APIView):
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)

    def get(self, request):
        context = dict()
        context['err_code'] = 0
        user = request.user
        if user.is_anonymous:
            context['err_code'] = 1001
            context['error'] = "您还未登录"
            return Response(context)
        data = request.GET
        id = data.get('id')
        if id is None:
            context['err_code'] = 2001
            context['error'] = "请求参数不正确"
            return Response(context)
        try:
            id = int(id)
        except:
            context['err_code'] = 2002
            context['error'] = "参数格式不正确"
            return Response(context)
        group = GroupModel.objects.filter(id=id)
        if not group.exists():
            context['err_code'] = 4004
            context['error'] = "该小组不存在"
            return Response(context)
        group = group.first()
        if user != group.owner:
            context['err_code'] = 4003
            context['error'] = "没有权限执行该操作"
            return Response(context)
        context['data'] = GroupMembersSerializer(group).data['members']
        return Response(context)

    def delete(self, request):
        context = dict()
        context['err_code'] = 0
        user = request.user
        if user.is_anonymous:
            context['err_code'] = 1001
            context['error'] = "您还未登录"
            return Response(context)
        data = QueryDict(request.body)
        gid = data.get('group_id')
        uid = data.get('user_id')
        if gid is None or uid is None:
            context['err_code'] = 2001
            context['error'] = "请求参数不正确"
            return Response(context)
        try:
            uid = int(uid)
            gid = int(gid)
        except:
            context['err_code'] = 2002
            context['error'] = "参数格式不正确"
            return Response(context)
        member=GroupMembersModel.objects.filter(user__id=uid,group__id=gid)
        group = GroupModel.objects.filter(id=gid)
        if not member.exists() or not group.exists():
            context['err_code'] = 4004
            context['error'] = "该成员不在您的小组"
            return Response(context)
        member = member.first()
        group=group.first()
        if user != group.owner:
            context['err_code'] = 4003
            context['error'] = "没有权限执行该操作"
            return Response(context)
        member.delete()
        return Response(context)

class MyGroupView(APIView):
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)

    def get(self, request):
        context = dict()
        context['err_code'] = 0
        data = request.GET
        user = request.user
        if user.is_anonymous:
            context['err_code'] = 1001
            context['error'] = "您还未登录"
            return Response(context)
        status = data.get('status')
        try:
            start = int(data.get('start')) - 1
            end = int(data.get('end'))
        except:
            context['err_code'] = 2002
            context['error'] = "参数格式不正确"
            return Response(context)
        if status is None or start is None or end is None:
            context['err_code'] = 2001
            context['error'] = "请求参数不正确"
            return Response(context)
        if status == "member":
            groups = GroupMembersModel.objects.order_by('-time').filter(user=user)[start:end]
            context['data'] = GroupsSerializer(groups, many=True).data
        elif status == "owner":
            groups = GroupModel.objects.order_by('-create_time').filter(owner=user)[start:end]
            context['data'] = CreateGroupsSerializer(groups, many=True).data
        else:
            context['err_code'] = 2001
            context['error'] = "请求参数不正确"
            return Response(context)
        return Response(context)

    def post(self, request):
        context = dict()
        context['err_code'] = 0
        data = request.POST
        user = request.user
        if user.is_anonymous:
            context['err_code'] = 1001
            context['error'] = "您还未登录"
            return Response(context)
        id = data.get('id')
        password = data.get('password')
        if id is None or password is None:
            context['err_code'] = 2001
            context['error'] = "请求参数不正确"
            return Response(context)
        try:
            id = int(id)
        except:
            context['err_code'] = 2002
            context['error'] = "参数格式不正确"
            return Response(context)
        group = GroupModel.objects.filter(id=id)
        if not group.exists():
            context['err_code'] = 4004
            context['error'] = "该小组不存在"
            return Response(context)
        group = group.first()
        if GroupMembersModel.objects.filter(user=user, group=group).exists():
            context['err_code'] = 4003
            context['error'] = "您已经加入该小组"
            return Response(context)
        if group.owner == user:
            context['err_code'] = 4003
            context['error'] = "不能加入自己创建的小组"
            return Response(context)
        if group.password != password:
            context['err_code'] = 4002
            context['error'] = "密码错误"
            return Response(context)
        GroupMembersModel.objects.create(user=user, group=group)
        return Response(context)


class MyGroupNumView(APIView):
    def get(self, request):
        context = dict()
        context['err_code'] = 0
        data = request.GET
        user = request.user
        if user.is_anonymous:
            context['err_code'] = 1001
            context['error'] = "您还未登录"
            return Response(context)
        status = data.get('status')
        if status is None:
            context['err_code'] = 2001
            context['error'] = "请求参数不正确"
            return Response(context)
        if status == "member":
            context['data'] = GroupMembersModel.objects.filter(user=user).count()
        elif status == "owner":
            context['data'] = GroupModel.objects.filter(owner=user).count()
        else:
            context['err_code'] = 2001
            context['error'] = "请求参数不正确"
            return Response(context)
        return Response(context)
