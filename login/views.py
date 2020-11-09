from django.contrib import auth
from .serializers import LoginSerializer,UserSerializer,RegisterSerializer
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
import logging
from rest_framework.authentication import SessionAuthentication,BasicAuthentication
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
class RegisterView(APIView):  # 注册相关视图类

    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)
    def post(self, request):
        context = dict()
        context['err_code']=0
        data = RegisterSerializer(data=request.POST)
        if not data.is_valid():  # 验证数据的有效性，如果无效证明绕过了前端
            context['err_code'] = 4002
            errors = data.errors
            key, value = get_first_error(errors)
            context['error'] = value[0]
            return Response(context)
        data = data.data
        username = data['username']
        password = data['password']
        nickname = data['nickname']
        if User.objects.filter(username=username).exists():
            context['error'] = "用户名已存在"
            context['err_code'] = 4002
            return Response(context)
        User.objects.create_user(username=username, password=password, first_name=nickname)
        context['err_code'] = 0
        context['data']=dict()
        context['data']['result']=True
        return Response(context)
    # def put(self,request):
    #     context = dict()
    #     context['err_code'] = 0
    #     user=request.user
    #     if user.is_anonymous:
    #         context['err_code'] = 1001
    #         context['error'] = "您还未登录"
    #         return Response(context)
    #     data = QueryDict(request.body)
    #     nickname = data.get("nickname")
    #     if nickname is None or re.match("^[\u4e00-\u9fa5·]{2,25}$", nickname) is None:
    #         context['err_code'] = 4002
    #         context['error']="数据不合法"
    #         return Response(context)
    #     user_model=User.objects.get(username=user.username)
    #     user_model.first_name=nickname
    #     user_model.save()
    #     return Response(context)

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

