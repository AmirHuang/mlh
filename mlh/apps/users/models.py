from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.
class User(AbstractUser):
    """用户模型类"""

    GENDER_CHOICES = (
        (0, 'male'),
        (1, 'female')
    )
    mobile = models.CharField(max_length=11, unique=True, default='', null=True, verbose_name='手机号')
    avatar = models.ImageField(default="./img/amir.png", verbose_name="用户头像")
    is_vip = models.BooleanField(default=False)
    like_news = models.ManyToManyField('news.NewsModel', related_name='followed_user', default=False,
                                       verbose_name="用户收藏的新闻")
    city = models.CharField(max_length=30, verbose_name='现居地址', null=True)
    school = models.CharField(max_length=20, verbose_name='毕业学校', null=True)
    experience = models.TextField(verbose_name='工作经历', null=True)
    gender = models.SmallIntegerField(choices=GENDER_CHOICES, default=0, verbose_name="性别")
    introduction = models.TextField(verbose_name='个人简介', null=True)
    education = models.TextField(verbose_name='教育经历', null=True)
    truename = models.CharField(max_length=5, verbose_name='真实姓名', null=True)
    birth = models.DateTimeField(verbose_name='出生日期', null=True)
    company = models.CharField(max_length=20, verbose_name='公司', null=True)
    personurl = models.CharField(max_length=20, verbose_name='个人网址', null=True)

    class Meta:
        db_table = 'tb_users'
        verbose_name = '用户'
        verbose_name_plural = verbose_name


class GoodAt(models.Model):
    """用户技能表"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='good_at', verbose_name='用户')
    skill = models.CharField(max_length=10, verbose_name='技能', null=True)

    class Meta:
        db_table = 'tb_good_at'
        verbose_name = '用户技能'
        verbose_name_plural = verbose_name


class UsersRelationship(models.Model):
    """用户关系模型表,关注,和被关注"""
    follower_id = models.ForeignKey(User, related_name="follower", verbose_name='此用户关注的用户', on_delete=models.CASCADE)
    followed_id = models.ForeignKey(User, related_name="followed", verbose_name='此用户被谁关注了', on_delete=models.CASCADE)

    class Meta:
        db_table = 'tb_follower'
        verbose_name = '用户关注关系'
        verbose_name_plural = verbose_name
