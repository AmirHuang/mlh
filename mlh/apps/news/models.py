from django.db import models

from users.models import User


class BaseModel(models.Model):
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    update_time = models.DateTimeField(auto_now=True, verbose_name="更新时间")

    class Meta:
        # 说明是抽象模型类, 用于继承使用，数据库迁移时不会创建BaseModel的表
        abstract = True


class NewsModel(BaseModel):
    """新闻的模型类"""
    author = models.ForeignKey('users.User', default=1, related_name='news', on_delete=models.CASCADE,
                               verbose_name="新闻作者")
    title = models.CharField(max_length=64, verbose_name="新闻标题")
    content = models.TextField(default="", verbose_name='新闻内容')
    category = models.ManyToManyField('CategoryModel', related_name='news',
                                      verbose_name='新闻的分类')
    is_delete = models.BooleanField(default=False, verbose_name="是否删除")
    click = models.IntegerField(default=0, verbose_name="点击量")
    source = models.CharField(max_length=32, default='官方发布', verbose_name="新闻来源")
    digest = models.CharField(max_length=1024, default='', verbose_name="新闻摘要")

    class Meta:
        db_table = 'tb_news'
        verbose_name = '新闻详情'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title


class CategoryModel(BaseModel):
    """新闻分类的表"""
    category_name = models.CharField(max_length=32, verbose_name="新闻分类名称")

    class Meta:
        db_table = 'tb_category'
        verbose_name = '新闻分类'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.category_name


class CommentModel(BaseModel):
    """评论的表"""
    user = models.ForeignKey('users.User', related_name='comment', on_delete=models.CASCADE, verbose_name="评论的用户")
    news = models.ForeignKey('NewsModel', related_name='comment', on_delete=models.CASCADE, verbose_name="被评论的新闻")
    parent_comment = models.ForeignKey('self', related_name='son_comment', null=True, blank=True,
                                       on_delete=models.CASCADE, verbose_name="此评论的父评论")
    conent = models.CharField(max_length=128, verbose_name='评论内容')

    class Meta:
        db_table = 'tb_comments'
        verbose_name = '新闻评论'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.conent


class ShareNews(BaseModel):
    """分享表"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="用户ID")
    sharnews = models.ForeignKey(NewsModel, on_delete=models.CASCADE, verbose_name="我的分享")

    class Meta:
        db_table = "tb_share_news"
        verbose_name = "分享新闻表"
        verbose_name_plural = '分享新闻表'
