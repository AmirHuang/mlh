import random
from django_redis import get_redis_connection
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView, GenericAPIView, RetrieveAPIView, UpdateAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated

from rest_framework.response import Response
from rest_framework.views import APIView

from celery_tasks.sms.tasks import send_sms_code
from news.models import ShareNews
from qs_answer.models import Answer, Question
from users.models import User
# from users.serializers import CreateUserSerializer, UserTopSerializer, UserDetailSerializer, UserAnswerSerlalizer, \
#     UserQuestionSerlalizer,UserFollewNewsSerlaizer, UserAcountSetSerializer, UserShareNewsSerlaizer
from users.serializers import UserTopSerializer, UserDetailSerializer
from . import serializers

from users.models import User
from users.serializers import CreateUserSerializer


class SmsCode(APIView):

    def get(self, request, mobile):
        # 1.从前端获取手机号
        # 2.对手机号进行正则校验
        # 3.生成短信验证码
        sms_code = '%06d' % random.randint(0, 999999)
        # print(sms_code)
        # 4.保存短信信息到ｒｅｄｉｓ数据中
        # 和redis数据库建立连接
        con = get_redis_connection('smscodes')
        flag = con.get('smscode_flag_%s' % mobile)
        # print('----flag', flag)
        if flag:
            return Response({'error': '请求过于频繁'})
        # 生成管道对象
        p1 = con.pipeline()
        # 保存短信验证码到redis中
        p1.setex('smscode_%s' % mobile, 300, sms_code)
        # 设置请求时效标志
        p1.setex('smscode_flag_%s' % mobile, 60, 1)
        # 执行管道（连接缓存， 存入数据）
        p1.execute()
        # 使用celery异步发送短信
        result_dic = send_sms_code(sms_code, mobile)
        return Response(result_dic)


class UserView(CreateAPIView):
    """用户注册，传入参数 username, password, sms_code, mobile, allow
    继承自CreateAPIView ，进行序列化和反序列化
    """
    serializer_class = CreateUserSerializer


class UsernameCountView(APIView):
    """校验用户是否存在的类视图"""

    def get(self, request, username):
        # 校验用户名的规则。不能是纯数字
        """把前端用get方法发送过来的用户名在数据库查询"""
        count = User.objects.filter(username=username).count()

        data = {'username': username,
                'count': count,
                }

        return Response(data=data)


class MobileCountView(APIView):
    """校验手机号数量"""

    def get(self, request, mobile):
        """获取指定的手机号的数量"""
        count = User.objects.filter(mobile=mobile).count()

        # # 查询出数量，并和用户名一起返回
        data = {
            'mobile': mobile,
            'count': count
        }
        return Response(data=data)


class UserTopView(RetrieveAPIView):
    #     个人界面上面部分ls
    #   未添加用户认证
    serializer_class = UserTopSerializer

    def get_object(self):
        return self.request.user


class UserDetailView(RetrieveAPIView, UpdateAPIView):
    # 用户详情
    serializer_class = UserDetailSerializer

    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user