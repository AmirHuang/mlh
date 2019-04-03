# _*_ coding: utf-8 _*_
# @time     : 2019/04/02
# @Author   : Amir
# @Site     : 
# @File     : urls.py
# @Software : PyCharm


# from django.conf.urls import url
from django.urls import path
from rest_framework_jwt.views import obtain_jwt_token

from . import views

urlpatterns = [
    path('sms_codes/<int:mobile>/', views.SmsCode.as_view()),
    path('usernames/<str:username>/count/', views.UsernameCountView.as_view()),
    path('mobiles/<int:mobile>/count/', views.MobileCountView.as_view()),
    path(r'users/', views.UserView.as_view()),
    path(r'user/top/', views.UserTopView.as_view()),
    # url(r'^user/answer/$', views.UserAnswerView.as_view()),
    # url(r'^user/questions/$', views.UserQuestionView.as_view()),
    path(r'user/myfile/', views.UserDetailView.as_view()),
    # url(r'^user/answer/$', views.UserAnswerView.as_view()),
    # url(r'^user/questions/$', views.UserQuestionView.as_view()),
    # url(r'^user/follewnews/$', views.UserFollewNewsView.as_view()),
    # url(r'^user/share/$', views.UserShareNewsView.as_view()),
    # url(r'^user/collection/$', views.UserShareNewsView.as_view()),
    # url(r'^user/acountset/$', views.UserAccountSetView.as_view()),
    # # url(r'^user/dynamic/$', views.UserDynamicView.as_view()),
    # # url(r'^authorizations/$', views.UserLoginAPIView.as_view()),
    # url(r'^authorizations/$', obtain_jwt_token),  # token签发
]