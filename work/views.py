from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import HomeWorkUpSerializer, HomeWorkInfSerializer, HomeWorkSerializer, HomeWorkCreateSerializer , DoneListSerializer
from common.common import get_first_error
from .models import HomeWorkInfModel, HomeWorkMembersModel
from datetime import datetime
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from django.http import QueryDict, FileResponse
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
        data = HomeWorkUpSerializer(data=request.POST)
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
            groups = request.POST.get('groups')
            if groups is None or len(groups) == 0:
                context['error'] = "至少选择一个小组"
                context['err_code'] = 2002
                return Response(context)
            groups = str(groups)
            groups = groups.split(',')
            groups_in = list()
            try:
                for group in groups:
                    group = int(group)
                    groups_in.append(group)
            except:
                context['error'] = "小组id只能为int"
                context['err_code'] = 2002
                return Response(context)

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
                                                                         ),

                                                       )
            for group_id in groups:
                homework.groups.add(group_id)
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
            querys = HomeWorkInfModel.objects.filter(id=id)
            if not querys.exists():  # 请求数据不存在
                context['err_code'] = 4004
                context['error'] = "无法找到您要的数据"
                return Response(context)
            query = querys.first()
            is_member = HomeWorkMembersModel.objects.filter(owner=user, work__id=id).exists()
            is_owner = (user == query.owner)
            if not is_member and not is_owner:
                context['err_code'] = 4003
                context['error'] = "您无权查看此内容"
                return Response(context)

            context['err_code'] = 0
            context['data'] = HomeWorkInfSerializer(query).data
            if is_owner:
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
        data = HomeWorkUpSerializer(data=put_data)
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
            querys = HomeWorkInfModel.objects.filter(id=id)
            if not querys.exists():  # 请求数据不存在
                context['err_code'] = 4004
                context['error'] = "无法找到您要的数据"
                return Response(context)
            query = querys.first()
            if user != query.owner:
                context['err_code'] = 4003
                context['error'] = "您无权执行此操作"
                return Response(context)
            querys.update(name=data['name'],
                          type=data['type'],
                          subject=data['subject'],
                          remark=data.get('remark') if data.get('remark') else '',
                          owner=user,
                          member_can_know_donelist=True if data[
                                                               'member_can_know_donelist'] == 'true' else False,
                          member_can_see_others=True if data[
                                                            'member_can_see_others'] == 'true' else False,
                          )
            query.end_time = datetime(year=int(end_time[0:4]),
                                      month=int(end_time[5:7]),
                                      day=int(end_time[8:10]),
                                      hour=int(end_time[11:13]),
                                      minute=int(end_time[14:16]))
            query.save()  # 没有这一行不能触发自动修改事件
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
            context['data'] = HomeWorkMembersModel.objects.filter(owner=user).count()
        elif status == 'notdone':
            context['data'] = HomeWorkMembersModel.objects.filter(owner=user, done=False).count()
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
            work = HomeWorkMembersModel.objects.filter(owner=user).order_by('-end_time')[start:end]
            context['data'] = HomeWorkSerializer(work, many=True).data
        elif status == "notdone":
            work = HomeWorkMembersModel.objects.filter(owner=user, done=False).order_by('-end_time')[start:end]
            context['data'] = HomeWorkSerializer(work, many=True).data
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
        print(work_id)
        try:
            work_id = int(work_id)
        except:
            context['err_code'] = 1002
            context['error'] = "请求参数不正确"
            return Response(context)
        done = HomeWorkMembersModel.objects.filter(work__id=work_id, owner=user)
        if not done.exists():
            context['err_code'] = 4004
            context['error'] = "您没有次参加本作业"
            return Response(context)
        done = done.first()
        file = request.FILES.get("file")  # 获取上传的文件，如果没有文件，则默认为None
        if not file:
            context['err_code'] = 2001
            context['error'] = "没有文件"
            return Response(context)
        dir_path = os.path.join(os.getcwd(), "file", str(datetime.now().year), str(datetime.now().month),
                                str(done.work.id))
        file_name = user.username + user.first_name + os.path.splitext(file.name)[1]
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
        path = os.path.join(dir_path, file_name)
        if done.done:
            last_file = os.path.join(dir_path, done.file_name)
            if os.path.exists(last_file):
                os.remove(last_file)
        done.done = True
        done.file_name = file_name
        done.upload_time = datetime.now()
        done.save()
        destination = open(path, 'wb+')
        for chunk in file.chunks():
            destination.write(chunk)
        destination.close()
        return Response(context)

    def get(self, request):
        context = dict()
        context['err_code'] = 0
        data = request.GET
        user = request.user
        if user.is_anonymous:
            context['err_code'] = 1001
            context['error'] = "您还未登录"
            return Response(context)
        work_id = data.get('work_id')
        print(work_id)
        try:
            work_id = int(work_id)
        except:
            context['err_code'] = 1002
            context['error'] = "请求参数不正确"
            return Response(context)
        done = HomeWorkMembersModel.objects.filter(work__id=work_id, owner=user)
        if not done.exists():
            context['err_code'] = 4004
            context['error'] = "您没有次参加本作业"
            return Response(context)
        done = done.first()
        context['data'] = dict()
        context['data']['done'] = done.done
        context['data']['file_name'] = done.file_name
        context['data']['work_name'] = done.work.name
        context['data']['upload_time'] = done.upload_time
        return Response(context)


class DownloadView(APIView):
    def get(self, request):
        context = dict()
        context['err_code'] = 0
        data = request.GET
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
        done = HomeWorkMembersModel.objects.filter(work__id=work_id, owner=user)
        if not done.exists():
            context['err_code'] = 4004
            context['error'] = "您没有次参加本作业"
            return Response(context)
        done = done.first()
        if not done.done:
            context['err_code'] = 4004
            context['error'] = "您还没有提交本次作业"
            return Response(context)
        dir_path = os.path.join(os.getcwd(), "file", str(datetime.now().year), str(datetime.now().month),
                                str(done.work.id))
        file_name = done.file_name
        file = os.path.join(dir_path, file_name)
        if not os.path.exists(file):
            context['err_code'] = 4004
            context['error'] = "很抱歉，该文件已过期被清理"
            return Response(context)

        file = open(file, 'rb')
        response = FileResponse(file)
        response['Content-Type'] = 'application/octet-stream'
        response['Content-Disposition'] = "attachment; filename= {}".format(file_name)
        return response

class ExportView(APIView):
    def get(self, request):
        context = dict()
        context['err_code'] = 0
        data = request.GET
        user = request.user
        if user.is_anonymous:
            context['err_code'] = 1001
            context['error'] = "您还未登录"
            return Response(context)
        work_id = data.get('work_id')
        user_id=data.get('user_id')
        try:
            work_id = int(work_id)
        except:
            context['err_code'] = 1002
            context['error'] = "请求参数不正确"
            return Response(context)
        if user_id is not None: # 如果同时附带user_id，那就是点击了下载单个用户文件
            try:
                user_id=int(user_id)
            except:
                context['err_code']= 1002
                context['error'] = "请求参数不正确"
                return Response(context)
            file_name_upload=data.get('file_name')
            if file_name_upload is None:
                context['err_code'] = 1002
                context['error'] = "请求参数不正确，没有文件名"
                return Response(context)
            done = HomeWorkMembersModel.objects.filter(work__id=work_id, owner__id=user_id)
            if not done.exists():
                context['err_code'] = 4004
                context['error'] = "该用户没有参与本次作业"
                return Response(context)
            done = done.first()
            if not done.done:
                context['err_code'] = 4004
                context['error'] = "该用户还没有完成本次作业"
                return Response(context)
            dir_path = os.path.join(os.getcwd(), "file", str(datetime.now().year), str(datetime.now().month),
                                    str(done.work.id))
            file_name = done.file_name
            if file_name != file_name_upload:
                context['err_code'] = 3001
                context['error'] = "该文件已发生变化，请刷新页面重试"
                return Response(context)
            file = os.path.join(dir_path, file_name)
            if not os.path.exists(file):
                context['err_code'] = 4004
                context['error'] = "很抱歉，该文件已过期被清理"
                return Response(context)

            file = open(file, 'rb')
            response = FileResponse(file)
            response['Content-Type'] = 'application/octet-stream'
            response['Content-Disposition'] = "attachment; filename= {}".format(file_name)
            return response
        else: # 如果user_id为None，那么可以认为是导出操作
            pass


class DoneListView(APIView):
    def get(self,request):
        context = dict()
        context['err_code'] = 0
        data = request.GET
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
        work=HomeWorkInfModel.objects.filter(id=work_id).order_by('done')
        if not work.exists():
            context['err_code'] = 4004
            context['error'] = "没有找到请求的作业"
            return Response(context)
        work=work.first()
        if user != work.owner:
            context['err_code'] = 4003
            context['error'] = "您没有权限查看该内容"
            return Response(context)
        done = HomeWorkMembersModel.objects.filter(work__id=work_id).order_by('done','-upload_time')
        data=DoneListSerializer(done,many=True).data
        context['data']=data
        return Response(context)