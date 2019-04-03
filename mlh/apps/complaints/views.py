# _*_ coding: utf-8 _*_
# @time     : 2019/04/02
# @Author   : Amir
# @Site     :
# @File     : urls.py
# @Software : PyCharm

from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from rest_framework import status
from rest_framework.generics import GenericAPIView, CreateAPIView, DestroyAPIView
from rest_framework.mixins import CreateModelMixin, DestroyModelMixin

from rest_framework.generics import ListAPIView, RetrieveAPIView

from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from news.utils import StandardResultsSetPagination
from .serializers import ComplaintSerializer, CommentSerializer, ComplaintLikeSerializer, ComplaintCollectionSerializer, \
    ComplaintCommentLikeSerializer
from .models import ComplaintModel, ComplaintLikeModel, ComplaintCollectionModel, CommentModel, \
    ComplaintCommentLikeModel


class ComplaintViewSet(ModelViewSet):
    """
    吐槽列表
    """
    serializer_class = ComplaintSerializer
    queryset = ComplaintModel.objects.all()

    pagination_class = StandardResultsSetPagination

    def list(self, request, *args, **kwargs):
        # 获取用户信息
        user = request.user
        user_likes_list = []  # 用户点赞
        user_collections_list = []  # 用户收藏
        # 判断用户是否登录
        print(user)
        if user is not None:
            # 获取用户的点赞记录
            user_likes = ComplaintLikeModel.objects.filter(user=user.id).only('complaint')
            for user_like in user_likes:
                user_likes_list.append(user_like.complaint.id)
                print('user_likes_list: ', user_likes_list)
            # 获取用户的收藏记录
            user_collections = ComplaintCollectionModel.objects.filter(user=user.id).only('complaint')
            for user_collection in user_collections:
                user_collections_list.append(user_collection.complaint.id)
        # 分页
        page = self.paginate_queryset(self.queryset)
        if page is not None:
            queryset = page
        else:
            queryset = self.queryset
            # serializer = self.get_serializer(page, many=True)
            # return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        # 添加是否点赞，是否收藏字段
        for complaint in serializer.data:
            # 判断是否点赞
            if complaint['id'] in user_likes_list:
                complaint['is_like'] = True
            else:
                complaint['is_like'] = False
            # 判断是否收藏
            if complaint['id'] in user_collections_list:
                complaint['is_collection'] = True
            else:
                complaint['is_collection'] = False
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        """
        吐槽详情
        """
        user = request.user
        user_likes_list = []  # 用户点赞
        user_collections_list = []  # 用户收藏
        # 判断用户是否登录
        if user is not None:
            # 获取用户的点赞记录
            user_likes = ComplaintLikeModel.objects.filter(user=user.id).only('complaint')
            for user_like in user_likes:
                user_likes_list.append(user_like.complaint.id)
            # 获取用户的收藏记录
            user_collections = ComplaintCollectionModel.objects.filter(user=user.id).only('complaint')
            for user_collection in user_collections:
                user_collections_list.append(user_collection.complaint.id)

        queryset = self.get_object()
        serializer = self.get_serializer(queryset)
        # 添加是否点赞，是否收藏字段
        data = dict(serializer.data)
        # 判断是否点赞
        if data['id'] in user_likes_list:
            data['is_like'] = True
        else:
            data['is_like'] = False
        # 判断是否收藏
        if data['id'] in user_collections_list:
            data['is_collection'] = True
        else:
            data['is_collection'] = False
        return Response(data)

    # def create(self, request, *args, **kwargs):
    #     """
    #     新建吐槽
    #     """
    #     user = request.user
    #     request.data['author_id'] = user.id
    #     print(request.data)
    #     serializer = self.get_serializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     print(serializer.data)
    #     self.perform_create(serializer)
    #     headers = self.get_success_headers(serializer.data)
    #     return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class CommentView(CreateAPIView):
    """
    吐槽评论
    """
    serializer_class = CommentSerializer
    queryset = CommentModel.objects.all()
    pagination_class = StandardResultsSetPagination

    def get(self, request, complaint):
        # 获取用户信息
        user = request.user
        user_likes_list = []  # 用户点赞
        # 判断用户是否登录

        if user is not None:
            user_likes = ComplaintCommentLikeModel.objects.filter(user=user.id).only('comment')
            for user_like in user_likes:
                user_likes_list.append(user_like.comment.id)
        queryset = self.get_queryset().filter(complaint=complaint)
        # 分页
        page = self.paginate_queryset(queryset)
        if page is not None:
            queryset = page

        serializer = self.get_serializer(queryset, many=True)
        # 添加是否点赞，是否收藏字段
        for complaint in serializer.data:
            # 判断是否点赞
            if complaint['id'] in user_likes_list:
                complaint['is_like'] = True
            else:
                complaint['is_like'] = False

        return Response(serializer.data)


class ComplaintLikeView(CreateAPIView, DestroyAPIView):
    """
    吐槽点赞
    """
    serializer_class = ComplaintLikeSerializer
    queryset = ComplaintLikeModel.objects.all()

    def post(self, request, *args, **kwargs):
        """
        点赞
        """
        try:
            respone = super().post(request, *args, **kwargs)
            complaint = request.data['complaint']
            comp = ComplaintModel.objects.get(id=complaint)
            comp.like_count += 1
            comp.save()
        except Exception as e:
            raise e
        else:
            return respone

    def destroy(self, request, complaint, *args, **kwargs):
        """
        取消点赞
        """
        # complaint = self.get_object()
        complaint_like = self.queryset.filter(complaint=complaint, user=request.user.id)
        # 如过记录存在
        if complaint_like:
            complaint_like.delete()
            # 对应相关吐槽点赞数-1
            comp = ComplaintModel.objects.get(id=complaint)
            comp.like_count -= 1
            comp.save()
            return Response(status=200)
        return Response(status=400)


class ComplaintCollectionView(CreateAPIView, DestroyAPIView):
    """
    吐槽收藏
    """
    serializer_class = ComplaintCollectionSerializer
    queryset = ComplaintCollectionModel.objects.all()

    def post(self, request, *args, **kwargs):
        """
        点赞
        """
        try:
            respone = super().post(request, *args, **kwargs)
            complaint = request.data['complaint']
            comp = ComplaintModel.objects.get(id=complaint)
            comp.collection_count += 1
            comp.save()
        except Exception as e:
            raise e
        else:
            return respone

    def destroy(self, request, complaint, *args, **kwargs):
        """
        取消收藏
        """
        complaint_collection = self.queryset.filter(complaint=complaint, user=request.user.id)
        # 如过记录存在
        if complaint_collection:
            complaint_collection.delete()
            # 对应相关吐槽点赞数-1
            comp = ComplaintModel.objects.get(id=complaint)
            comp.collection_count -= 1
            comp.save()
            return Response(status=200)
        return Response(status=400)


class ComplaintCommentLikeView(CreateAPIView, DestroyAPIView):
    """
    吐槽评论点赞
    """
    serializer_class = ComplaintCommentLikeSerializer
    queryset = ComplaintCommentLikeModel.objects.all()

    # 点赞,,相关评论数+1
    def post(self, request, *args, **kwargs):

        try:
            respone = super().post(request, *args, **kwargs)
            comment = request.data['comment']
            comm = CommentModel.objects.get(id=comment)
            comm.like_count += 1
            comm.save()
        except Exception as e:
            raise e
        else:
            return respone

    def destroy(self, request, complaintcomment, *args, **kwargs):
        """
        取消评论点赞
        """

        complaint_comment_like = self.queryset.filter(comment=complaintcomment, user=request.user.id)
        if complaint_comment_like:
            complaint_comment_like.delete()

            # 取消点赞,相关评论数-1
            comm = CommentModel.objects.get(id=complaintcomment)
            comm.like_count -= 1
            comm.save()
            return Response(status=200)
        return Response(status=400)
