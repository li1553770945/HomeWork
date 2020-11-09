from rest_framework.views import APIView, Response
from .serializers import GroupSerializer, GroupsSerializer, CreateGroupsSerializer, GroupUnSerializer, \
    valid_group_information
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
            context['err_code'] = 3004
            context['error'] = "无法找到您要的数据"
            return Response(context)
        group = query.first()
        is_member = GroupMembersModel.objects.filter(user=user, group=group).exists()
        is_owner = (group.owner == user)
        if not is_member and not is_owner:
            context['err_code'] = 3003
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
        GroupModel.objects.create(owner=user, name=data['name'], desc=data['desc'], password=data['password'])
        return Response(context)

    def put(self, request):
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
        password = data.get('password')
        name = data.get('name')
        desc = data.get('desc')
        delete_user_id = data.get('delete_user_id')
        if password is None and name is None and desc is None and delete_user_id is None:
            context['err_code'] = 2001
            context['error'] = "请求参数不正确"
            return Response(context)
        group = GroupModel.objects.filter(id=id)
        if not group.exists():
            context['err_code'] = 4004
            context['error'] = "该小组不存在"
            return Response(context)
        group = group.first()
        if user != group.owner:
            context['err_code'] = 4003
            context['error'] = "您无权操作"
            return Response(context)
        if password is not None:
            if not valid_group_information('password', password):
                context['err_code'] = 2002
                context['error'] = "格式不正确"
                return Response(context)
            group.password = password
        if name is not None:
            if not valid_group_information('name', name):
                context['err_code'] = 2002
                context['error'] = "格式不正确"
                return Response(context)
            group.name = name
        if desc is not None:
            if not valid_group_information('desc', desc):
                context['err_code'] = 2002
                context['error'] = "格式不正确"
                return Response(context)
            group.desc = desc
        group.save()
        if delete_user_id is not None:
            try:
                delete_user_id = int(delete_user_id)
            except:
                context['err_code'] = 2002
                context['error'] = "参数格式不正确"
                return Response(context)
            delete_user = GroupMembersModel.objects.filter(group_id=id, user_id=delete_user_id)
            if not delete_user.exists():
                context['err_code'] = 4004
                context['error'] = "用户不存在或不在您的组织"
                return Response(context)
            delete_user.delete()
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
            context['data'] = GroupMembersModel.objects.order_by('-time').filter(user=user).count()
        elif status == "owner":
            context['data'] = GroupModel.objects.order_by('-create_time').count()
        else:
            context['err_code'] = 2001
            context['error'] = "请求参数不正确"
            return Response(context)
        return Response(context)
