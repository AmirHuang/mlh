# _*_ coding: utf-8 _*_
# @time     : 2019/04/02
# @Author   : Amir
# @Site     : 
# @File     : serializers.py
# @Software : PyCharm

import re

from django_redis import get_redis_connection
from rest_framework import serializers

from rest_framework_jwt.settings import api_settings

# from news.serializers import NewsDeatilSerializer
from news.models import ShareNews

from qs_answer.models import Answer, Question
# from news.serializers import NewsSerializer
from .models import User


class CreateUserSerializer(serializers.ModelSerializer):
    """这是创建用户的序列化器"""
    # 说明这3个字段只是从前端发送过来校验，不需要返回
    sms_code = serializers.CharField(label="短信验证码", write_only=True)
    allow = serializers.CharField(label="同意协议", write_only=True)
    # 只在返回前端的时候使用。不需要进行校验和写入数据库。read_only=True
    token = serializers.CharField(label='登录状态token', read_only=True)  # 增加token字段

    # username = serializers.CharField(label='用户名',read_only=True)
    avatar = serializers.CharField(label='头像', read_only=True)
    is_vip = serializers.BooleanField(label='是否是vip', read_only=True)
    is_followed = serializers.BooleanField(label='是否关注', read_only=True)

    class Meta:
        # 指明用哪一个模型类对象
        model = User
        # 添加需要的字段
        fields = (
            'id', 'username', 'password', 'sms_code', 'mobile', 'allow', 'token', 'avatar', 'is_vip')

        extra_kwargs = {
            'username': {
                'min_length': 5,
                'max_length': 20,
                'error_messages': {
                    'min_length': '仅允许5-20个字符的用户名',
                    'max_length': '仅允许5-20个字符的用户名',
                }
            },
            'password': {
                'write_only': True,
                'min_length': 8,
                'max_length': 20,
                'error_messages': {
                    'min_length': '仅允许8-20个字符的密码',
                    'max_length': '仅允许8-20个字符的密码',
                }
            },
            'like_news': {
                'read_only': True
            }
        }

    def validate_username(self, value):
        """校验用户名"""
        try:
            value = int(value)
        except ValueError:
            return value
        raise serializers.ValidationError("用户名不能是纯数字！")

    def validate_mobile(self, value):
        """验证手机号"""
        if not re.match(r'^1[3-9]\d{9}$', value):
            raise serializers.ValidationError('手机号格式错误')
        return value

    def validate_allow(self, value):
        """检查用户是否同意协议"""
        if value != 'true':
            raise serializers.ValidationError('请同意用户使用协议！')
        return value

    # 校验用户名，不能和手机号一样
    # def validate_username(self,value):

    def validate(self, data):
        # 判断短信验证码
        # 获取redis的连接对象
        redis_conn = get_redis_connection('verify_codes')
        # 取到手机号码
        mobile = data['mobile']
        # 在redis中取到真实的短信验证码进行对比
        real_sms_code = redis_conn.get('sms_%s' % mobile)

        if not real_sms_code:
            raise serializers.ValidationError('短信验证码错误！')
        if data['sms_code'] != real_sms_code.decode():
            raise serializers.ValidationError('短信验证码错误！')

        return data

    def create(self, validated_data):
        """创建用户"""
        # 删除不需要保存在数据库中的字段
        del validated_data['sms_code']
        del validated_data['allow']
        # 调用父类创建模型对象
        user = super().create(validated_data)
        # 调用django的认真系统加密密码
        user.set_password(validated_data['password'])
        user.save()
        # 补充生成记录登录状态的token
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
        payload = jwt_payload_handler(user)
        token = jwt_encode_handler(payload)
        # 动态给user添加一个token属性
        user.token = token
        return user


class UserTopSerializer(serializers.ModelSerializer):
    # 个人头部信息
    class Meta:
        model = User
        exclude = ('password',)


class UserDetailSerializer(serializers.ModelSerializer):
    #     个人详情界面
    class Meta:
        model = User
        exclude = ('password',)


class UserSerializer(serializers.ModelSerializer):
    '''用户序列化器'''

    class Meta:
        model = User
        fields = '__all__'
