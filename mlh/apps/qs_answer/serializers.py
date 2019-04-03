from rest_framework import serializers

from qs_answer.models import Question


class QuestionListLatestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ["id", "title", "create_time", "publisher", "page_view", "approval_count"]


class QuestionListHotSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ["id", "title", "create_time", "publisher", "page_view", "approval_count"]


class QuestionListWatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ["id", "title", "create_time", "publisher", "page_view", "approval_count"]
