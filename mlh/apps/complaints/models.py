from django.db import models
from users.models import User


class BaseModel(models.Model):
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    update_time = models.DateTimeField(auto_now=True, verbose_name="更新时间")

    class Meta:
        # 说明是抽象模型类, 用于继承使用，数据库迁移时不会创建BaseModel的表
        abstract = True


# Create your models here.
class ComplaintModel(BaseModel):
    """
    吐槽
    """
    content = models.TextField(verbose_name="内容")
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="complaints", verbose_name="作者")
    like_count = models.IntegerField(verbose_name="点赞数", default=0)
    share_count = models.IntegerField(verbose_name="分享数", default=0)
    collection_count = models.IntegerField(verbose_name="收藏数", default=0)
    comment_count = models.IntegerField(verbose_name="评论数", default=0)

    class Meta:
        db_table = "tb_complaints"
        verbose_name = "吐槽"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.content


class CommentModel(BaseModel):
    """
    吐槽评论
    """
    content = models.TextField(verbose_name="内容")
    complaint = models.ForeignKey(ComplaintModel, on_delete=models.CASCADE, related_name="comments",
                                  verbose_name="所属吐槽")
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="complaint_comments", verbose_name="作者")
    like_count = models.IntegerField(verbose_name="点赞数", default=0)

    class Meta:
        db_table = "tb_complaint_comments"
        verbose_name = "吐槽评论"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.content


class ComplaintLikeModel(models.Model):
    """
    吐槽点赞
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="用户")
    complaint = models.ForeignKey(ComplaintModel, on_delete=models.CASCADE, verbose_name="所属吐槽")

    class Meta:
        db_table = "tb_complaint_likes"
        verbose_name = "吐槽点赞"
        verbose_name_plural = verbose_name
        unique_together = ('user', 'complaint')  # 作为联合主键


class ComplaintCollectionModel(models.Model):
    """
    吐槽收藏
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="用户")
    complaint = models.ForeignKey(ComplaintModel, on_delete=models.CASCADE, verbose_name="所属吐槽")

    class Meta:
        db_table = "tb_complaint_collections"
        verbose_name = "吐槽收藏"
        verbose_name_plural = verbose_name
        unique_together = ('user', 'complaint')  # 作为联合主键


class ComplaintCommentLikeModel(models.Model):
    """
    吐槽评论点赞
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="用户")
    comment = models.ForeignKey(CommentModel, on_delete=models.CASCADE, verbose_name="所属吐槽")

    class Meta:
        db_table = "tb_complaint_comment_likes"
        verbose_name = "吐槽评论点赞"
        verbose_name_plural = verbose_name
        unique_together = ('user', 'comment')
