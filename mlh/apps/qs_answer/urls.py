# _*_ coding: utf-8 _*_
# @time     : 2019/04/03
# @Author   : Amir
# @Site     : 
# @File     : urls.py
# @Software : PyCharm


from django.conf.urls import url
from . import views
urlpatterns=[
    url('^questions/latest', views.QuestionListLatestView.as_view()),
    url('^questions/hot', views.QuestionListHotView.as_view()),

]