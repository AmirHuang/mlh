# _*_ coding: utf-8 _*_
# @time     : 2019/04/02
# @Author   : Amir
# @Site     : 
# @File     : urls.py
# @Software : PyCharm

from django.conf.urls import url

from complaints import views

urlpatterns = [
    url(r"^complaints/$", views.ComplaintViewSet.as_view({'get': 'list', 'post': 'create'})),
    url(r"^complaints/(?P<pk>\d+)/$", views.ComplaintViewSet.as_view({'get': 'retrieve'})),
    url(r'^complaint/(?P<complaint>\d+)/comments/$', views.CommentView.as_view()),  # 吐槽评论&增加和查找
    url(r'^complaint/likes/$', views.ComplaintLikeView.as_view()),  # 吐槽点赞
    url(r'^complaint/likes/(?P<complaint>\d+)/$', views.ComplaintLikeView.as_view()),  # 取消点赞
    url(r'^complaint/collections/$', views.ComplaintCollectionView.as_view()),  # 吐槽收藏
    url(r'^complaint/collections/(?P<complaint>\d+)/$', views.ComplaintCollectionView.as_view()),  # 取消点赞
    url(r'^complaint/commentlikes/$', views.ComplaintCommentLikeView.as_view()),  # 吐槽评论点赞
    url(r'^complaint/commentlikes/(?P<complaintcomment>\d+)/$', views.ComplaintCommentLikeView.as_view()),  # 取消评论点赞
]
