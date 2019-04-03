# _*_ coding: utf-8 _*_
# @time     : 2019/04/02
# @Author   : Amir
# @Site     : 
# @File     : serializers.py
# @Software : PyCharm

from rest_framework import serializers

from complaints.models import ComplaintModel, CommentModel, ComplaintLikeModel, ComplaintCollectionModel, \
    ComplaintCommentLikeModel
from users.models import User

from . import models


class UserSerializer(serializers.ModelSerializer):
    avatar = serializers.CharField()

    class Meta:
        model = User
        fields = ('id', 'username', 'avatar')


class ComplaintSerializer(serializers.ModelSerializer):
    """
    吐槽序列化器
    """
    # user_id = UserSerializer(read_only=True)
    author = UserSerializer(read_only=True)

    class Meta:
        model = ComplaintModel
        fields = ('id', 'content', 'author', 'like_count', 'share_count', 'collection_count', 'comment_count')
        extra_kwargs = {
            'like_count': {
                'read_only': True
            },
            'share_count': {
                'read_only': True
            },
            'collection_count': {
                'read_only': True
            },
            'comment_count': {
                'read_only': True
            }
        }

    def create(self, validated_data):
        print('validated_data', validated_data)
        author_id = self.context['request'].user.id
        validated_data['author_id'] = author_id
        return super().create(validated_data)


class CommentSerializer(serializers.ModelSerializer):
    """
    吐槽评论序列化器
    """
    complaint_id = serializers.IntegerField()
    author = UserSerializer(read_only=True)

    class Meta:
        model = CommentModel
        fields = ('id', 'content', 'complaint_id', 'create_time', 'like_count', 'author')
        extra_kwargs = {
            'like_count': {
                'read_only': True
            },
            'create_time': {
                'read_only': True
            },
            'complaint_id': {
                'write_only': True
            }
        }

    def create(self, validated_data):
        print(self.context['request'].user)
        validated_data['author_id'] = self.context['request'].user.id
        try:
            resp = super().create(validated_data)
            complaint = validated_data['complaint_id']

            # 添加评论,评论数+1
            comp = ComplaintModel.objects.get(id=complaint)
            comp.comment_count += 1
            comp.save()
        except Exception as e:
            raise e
        else:
            return resp


class ComplaintLikeSerializer(serializers.ModelSerializer):
    """
    吐槽点赞序列化器
    """

    class Meta:
        model = ComplaintLikeModel
        fields = ('id', 'complaint')

    # 获取用户登录的相关信息
    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)

    def validate_complaint(self, value):
        """校验所属吐槽"""
        if not ComplaintModel.objects.get(id=value.id):
            raise serializers.ValidationError('吐槽内容不存在')
        return value


class ComplaintCollectionSerializer(serializers.ModelSerializer):
    """
    吐槽收藏序列化器
    """

    class Meta:
        model = ComplaintCollectionModel
        fields = ('id', 'complaint')

    # 获取用户登录的相关信息
    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)

    def validate_complaint(self, value):
        """校验所属吐槽"""
        if not ComplaintModel.objects.get(id=value.id):
            raise serializers.ValidationError('吐槽内容不存在')

        return value


class ComplaintCommentLikeSerializer(serializers.ModelSerializer):
    """
    吐槽评论点赞序列化器
    """

    class Meta:
        model = ComplaintCommentLikeModel
        fields = ('id', 'comment')

    # 获取用户登录的相关信息
    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user

        return super().create(validated_data)

    def validate_comment(self, value):
        """校验所属评论"""
        if not CommentModel.objects.get(id=value.id):
            raise serializers.ValidationError('吐槽内容不存在')

        return value
