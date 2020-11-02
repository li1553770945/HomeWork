from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import HomeWorkSerializer,HomeWorkInfSerializer
from common.common import get_first_error
from .models import HomeWorkInfModel
from datetime import datetime
from rest_framework.authentication import SessionAuthentication, BasicAuthentication


class CsrfExemptSessionAuthentication(SessionAuthentication):

    def enforce_csrf(self, request):
        return
# Create your views here.
from django.views.decorators.csrf import csrf_exempt


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
            data=data.data
            end_time=data['end_time']
            HomeWorkInfModel.objects.create(name=data['name'],
                                            type=data['type'],
                                            subject=data['subject'],
                                            remark=data.get('remark') if data.get('remark') else '',
                                            owner=user,
                                            member_can_know_donelist=True if data['member_can_know_donelist']=='true' else False,
                                            member_can_see_others=True if data['member_can_see_others']=='true' else False,
                                            end_time=datetime(year=int(end_time[0:4]),
                                                              month=int(end_time[5:7]),
                                                              day=int(end_time[8:10]),
                                                              hour=int(end_time[11:13]),
                                                              minute=int(end_time[14:16])
                                                              )
                                            )
            return Response(context)

    def get(self, request):
        context = dict()
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
            context['data'] = HomeWorkInfSerializer(query).data
            return Response(context)
    def put(self, request):
        pass

    def delete(self, request):
        pass
