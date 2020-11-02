from django.contrib import auth
from .serializers import LoginSerializer,UserSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
import logging
from rest_framework.authentication import SessionAuthentication
from common.common import get_first_error


class CsrfExemptSessionAuthentication(SessionAuthentication):

    def enforce_csrf(self, request):
        return


logger = logging.getLogger(__name__)


class LoginView(APIView):  # 登录相关视图类
    def post(self, request):  # 用户登录，提交post数据
        context = dict()
        data = LoginSerializer(data=request.POST)
        if not data.is_valid():  # 验证有效性
            errors = data.errors
            key, value = get_first_error(errors)
            context['error'] = value[0]
            context['err_code'] = 2002
        else: # 数据有效
            context['data'] = dict()
            data = data.data
            username = data['username']
            password = data['password']
            user = auth.authenticate(username=username, password=password)
            if user is None: # 用户名或密码错误
                context['data']['error'] = "用户名或密码错误"
                context['data']['result'] = False
            else:  # 验证通过
                auth.login(request, user)
                context['data']['name'] = request.user.get_short_name()
                context['data']['result'] = True
            context['err_code'] = 0
        return Response(context)

    def get(self, request):  # 检测用户是否登录
        context = dict()
        if not request.user.is_anonymous: #已经登录
            context['err_code'] = 0
            context['data'] = dict()
            context['data']['name'] = request.user.get_short_name()
            context['data']['result'] = True
        else:
            context = dict()
            context['err_code'] = 0
            context['data'] = dict()
            context['data']['result'] = False
        return Response(context)


class LogOutView(APIView):  # 登出
    def get(self, request):
        auth.logout(request)
        context = dict()
        context['err_code'] = 0
        context['data'] = dict()
        context['data']['result'] = True
        return Response(context)


class MeView(APIView):
    def get(self, request):
        context = dict()
        context['err_code'] = 0
        if not request.user.is_authenticated:
            context['err_code'] = 1001
            context['error'] = "您还未登录，请先登录"
            return Response(context)
        user = request.user
        user_serializer = UserSerializer(user)
        context['data'] = user_serializer.data
        return Response(context)

