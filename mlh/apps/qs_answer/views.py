from django.shortcuts import render

# Create your views here.
from rest_framework.generics import ListAPIView

from qs_answer.serializers import QuestionListLatestSerializer, QuestionListHotSerializer, QuestionListWatingSerializer
from . import models


class QuestionListLatestView(ListAPIView):
    serializer_class = QuestionListLatestSerializer

    # queryset = models.Question.objects.all()

    def get_queryset(self):
        return models.Question.objects.all().order_by("-create_time")  # 有问题，这里应该是最新回答的创建时间，而不是最新问题


class QuestionListHotView(ListAPIView):
    serializer_class = QuestionListHotSerializer

    # queryset = models.Question.objects.all()

    def get_queryset(self):
        question_list = models.Question.objects.all()


class QuestionListWatingView(ListAPIView):
    serializer_class = QuestionListWatingSerializer

    def get_queryset(self):
        # 查询回答数为0的问题列表，并以问题创建最新时间排序
        # 查询所有的问题列表，遍历问题列表，过滤出回答为0的问题，添加到新列表中。返回

        qs_all = models.Question.objects.all()
        for qs in qs_all:
            qs.answer_set.count()
