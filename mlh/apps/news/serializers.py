# _*_ coding: utf-8 _*_
# @time     : 2019/04/02
# @Author   : Amir
# @Site     : 
# @File     : serializers.py
# @Software : PyCharm

from rest_framework import serializers

from news.models import *
from users.models import User


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoryModel
        fields = ['category_name', 'id']
        # fields = '__all__'


class UserInfoSerializer(serializers.ModelSerializer):
    # 只在返回前端的时候使用。不需要进行校验和写入数据库。read_only=True
    username = serializers.CharField(label='用户名')
    avatar = serializers.CharField(label='用户头像')
    is_vip = serializers.BooleanField(label='是否是vip')

    class Meta:
        model = User
        fields = ['id', 'username', 'avatar', 'is_vip']


class NewsSerializer(serializers.ModelSerializer):
    author = UserInfoSerializer()
    category = CategorySerializer(many=True)
    followed_user = UserInfoSerializer(many=True)

    class Meta:
        model = NewsModel
        exclude = ['is_delete', 'content']


class CommentSerializer(serializers.ModelSerializer):
    """评论的序列化器"""
    user = UserInfoSerializer(read_only=True)  # 指明这个评论的用户的序列化器.

    # create_time = serializers.DateTimeField(label='创建时间',read_only=True)
    # comment_id = serializers.IntegerField(label='评论id')

    class Meta:
        model = CommentModel
        exclude = ['update_time']

    def validate(self, attrs):
        user_id = self.context['request'].user.id
        attrs['user_id'] = user_id

        return attrs


class NewsDeatilSerializer(serializers.ModelSerializer):
    author = UserInfoSerializer()
    category = CategorySerializer(many=True)

    # comment = CommentSerializer(many=True)  # 通过新闻查询这个新闻的所有的评论

    class Meta:
        model = NewsModel
        # fields = '__all__'
        exclude = ['is_delete']


class FollowerNewsSerializer(serializers.ModelSerializer):
    like_news = serializers.IntegerField(label='新闻的id')

    class Meta:
        model = User
        fields = ['id', 'like_news']
