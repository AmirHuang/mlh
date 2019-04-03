# _*_ coding: utf-8 _*_
# @time     : 2019/04/03
# @Author   : Amir
# @Site     : 
# @File     : urls.py
# @Software : PyCharm


from django.conf.urls import url

from news import views

urlpatterns = [
    url(r'^index/(?P<pk>\d*)$', views.IndexPage.as_view()),  # 首页数据
    url(r'^categories/$', views.GetCategory.as_view()),  # 获取分类列表
    url(r'^category/(?P<pk>\d*)', views.GetNews.as_view()),  # 获取指定分类下的新闻
    url(r'^news/(?P<pk>\d+)/$', views.NewsAPIView.as_view()),  # 获取指定新闻,发布一条新闻
    url(r'^comment/(?P<pk>\d+)/$', views.CommentView.as_view()),  # 获取指定新闻的评论
    url(r'^follow/$', views.FollowedNewsAPIView.as_view()),  # 关注一个新闻

]
