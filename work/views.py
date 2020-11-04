from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import HomeWorkSerializer, HomeWorkInfSerializer, HomeWorkAllSerializer, HomeWorkCreateSerializer
from common.common import get_first_error
from .models import HomeWorkInfModel
from datetime import datetime
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from django.http import QueryDict
import os


class CsrfExemptSessionAuthentication(SessionAuthentication):

    def enforce_csrf(self, request):
        return


class HomeWorkView(APIView):
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)

    def post(self, request):
        context = dict()
        user = request.user
        if user.is_anonymous:
            context['err_code'] = 1001
            context['error'] = "您还未登录"
            return Response(context)
        data = HomeWorkSerializer(data=request.POST)
        if not data.is_valid():  # 验证有效性
            errors = data.errors
            key, value = get_first_error(errors)
            context['error'] = key + ' ' + value[0]
            context['err_code'] = 2002
            return Response(context)
        else:
            context['err_code'] = 0
            data = data.data
            end_time = data['end_time']
            homework = HomeWorkInfModel.objects.create(name=data['name'],
                                                       type=data['type'],
                                                       subject=data['subject'],
                                                       remark=data.get('remark') if data.get('remark') else '',
                                                       owner=user,
                                                       member_can_know_donelist=True if data[
                                                                                            'member_can_know_donelist'] == 'true' else False,
                                                       member_can_see_others=True if data[
                                                                                         'member_can_see_others'] == 'true' else False,
                                                       end_time=datetime(year=int(end_time[0:4]),
                                                                         month=int(end_time[5:7]),
                                                                         day=int(end_time[8:10]),
                                                                         hour=int(end_time[11:13]),
                                                                         minute=int(end_time[14:16])
                                                                         )
                                                       )
            context['data'] = dict()
            context['data']['id'] = homework.id
            return Response(context)

    def get(self, request):
        context = dict()
        user = request.user
        if user.is_anonymous:
            context['err_code'] = 1001
            context['error'] = "您还未登录"
            return Response(context)
        id = request.GET.get('id')
        if id is None:  # 验证有效性
            context['error'] = "没有请求的作业id"
            context['err_code'] = 2002
            return Response(context)
        else:
            try:
                id = int(id)
            except:
                context['err_code'] = 2002
                context['error'] = "参数格式不正确"
                return Response(context)
            query = HomeWorkInfModel.objects.filter(id=id)
            if not query.exists():  # 请求数据不存在
                context['err_code'] = 4004
                context['error'] = "无法找到您要的数据"
                return Response(context)
            query = query.first()
            context['err_code'] = 0
            context['data'] = HomeWorkInfSerializer(query).data
            if user == query.owner:
                context['data'].update({'is_creater': True})
            else:
                context['data'].update({'is_creater': False})
            return Response(context)

    def put(self, request):
        context = dict()
        user = request.user
        if user.is_anonymous:
            context['err_code'] = 1001
            context['error'] = "您还未登录"
            return Response(context)
        put_data = QueryDict(request.body)
        data = HomeWorkSerializer(data=put_data)
        if not data.is_valid():  # 验证有效性
            errors = data.errors
            key, value = get_first_error(errors)
            context['error'] = key + ' ' + value[0]
            context['err_code'] = 2002
            return Response(context)
        else:
            context['err_code'] = 0
            data = data.data
            end_time = data['end_time']
            id = put_data.get('id')
            if id is None:
                context['error'] = "没有请求的作业id"
                context['err_code'] = 2002
                return Response(context)
            try:
                id = int(id)
            except:
                context['err_code'] = 2002
                context['error'] = "参数格式不正确"
                return Response(context)
            query = HomeWorkInfModel.objects.filter(id=id)
            if not query.exists():  # 请求数据不存在
                context['err_code'] = 4004
                context['error'] = "无法找到您要的数据"
                return Response(context)
            query = query.first()
            if user != query.owner:
                context['err_code'] = 4003
                context['error'] = "您无权执行此操作"
                return Response(context)
            HomeWorkInfModel.objects.update(name=data['name'],
                                            type=data['type'],
                                            subject=data['subject'],
                                            remark=data.get('remark') if data.get('remark') else '',
                                            owner=user,
                                            member_can_know_donelist=True if data[
                                                                                 'member_can_know_donelist'] == 'true' else False,
                                            member_can_see_others=True if data[
                                                                              'member_can_see_others'] == 'true' else False,
                                            end_time=datetime(year=int(end_time[0:4]),
                                                              month=int(end_time[5:7]),
                                                              day=int(end_time[8:10]),
                                                              hour=int(end_time[11:13]),
                                                              minute=int(end_time[14:16])
                                                              )
                                            )
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
            context['error'] = "没有请求的作业id"
            context['err_code'] = 2002
            return Response(context)
        try:
            id = int(id)
        except:
            context['err_code'] = 2002
            context['error'] = "参数格式不正确"
            return Response(context)
        query = HomeWorkInfModel.objects.filter(id=id)
        if not query.exists():  # 请求数据不存在
            context['err_code'] = 4004
            context['error'] = "无法找到您要的数据"
            return Response(context)
        query = query.first()
        if user != query.owner:
            context['err_code'] = 4003
            context['error'] = "您无权执行此操作"
            return Response(context)
        query.delete()
        return Response(context)


class MyHomeWorkNumView(APIView):
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
            context['data'] = HomeWorkInfModel.objects.filter().count()
        elif status == "owner":
            context['data'] = HomeWorkInfModel.objects.filter(owner=user).count()
        else:
            context['err_code'] = 2001
            context['error'] = "请求参数不正确"
            return Response(context)
        return Response(context)


class MyHomeWorkView(APIView):
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
            work = HomeWorkInfModel.objects.order_by('-end_time').filter()[start:end]
            context['data'] = HomeWorkAllSerializer(work, many=True).data
        elif status == "owner":
            work = HomeWorkInfModel.objects.order_by('-end_time').filter(owner=user)[start:end]
            context['data'] = HomeWorkCreateSerializer(work, many=True).data
        else:
            context['err_code'] = 2001
            context['error'] = "请求参数不正确"
            return Response(context)
        return Response(context)


class SubmitView(APIView):
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)

    def post(self, request):
        context = dict()
        context['err_code'] = 0
        data = request.POST
        user = request.user
        if user.is_anonymous:
            context['err_code'] = 1001
            context['error'] = "您还未登录"
            return Response(context)
        work_id = data.get('work_id')
        try:
            work_id = int(work_id)
        except:
            context['err_code'] = 1002
            context['error'] = "请求参数不正确"
            return Response(context)
        work = HomeWorkInfModel.objects.filter(id=work_id)
        if not work.exists():
            context['err_code'] = 4004
            context['error'] = "无法找到您提交的作业"
            return Response(context)
        work = work.first()

        file = request.FILES.get("file")  # 获取上传的文件，如果没有文件，则默认为None
        if not file:
            context['err_code'] = 2001
            context['error'] = "没有文件"
            return Response(context)
        dir_path = os.path.join(os.getcwd(), "file", str(datetime.now().year), str(datetime.now().month),
                                str(work.id) + work.name)
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
        path = os.path.join(dir_path, user.username + user.first_name + os.path.splitext(file.name)[1])
        destination = open(path, 'wb+')
        for chunk in file.chunks():
            destination.write(chunk)
        destination.close()
        return Response(context)
