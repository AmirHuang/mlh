from django.db import models

from users.models import User


class BaseModel(models.Model):
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    update_time = models.DateTimeField(auto_now=True, verbose_name="更新时间")
    approval_count = models.IntegerField(default=0, verbose_name="有用")
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, verbose_name="用户id")

    class Meta:
        # 说明是抽象模型类, 用于继承使用，数据库迁移时不会创建BaseModel的表
        abstract = True


class Question(BaseModel):
    """问题模型类"""
    title = models.CharField(max_length=200, unique=True, verbose_name="问题标题")
    view_count = models.IntegerField(default=0, verbose_name="浏览量")
    detail_info = models.TextField(verbose_name="提问详情")

    # label
    class Meta:
        db_table = "tb_questions"
        verbose_name = "问题"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title


class Answer(BaseModel):
    question = models.ForeignKey(Question, null=True, default="", on_delete=models.CASCADE, verbose_name="所属问题id")
    content = models.TextField(default="", verbose_name="回答内容")

    class Meta:
        db_table = "tb_answers"
        verbose_name = "回答"
        verbose_name_plural = verbose_name

    def __str__(self):
        return "%s" % self.id


class Tag_Category(models.Model):
    cate_name = models.CharField(max_length=30, default="", verbose_name="标签分类")

    class Meta:
        db_table = "tb_tag_categorys"
        verbose_name = "标签分类"
        verbose_name_plural = verbose_name


class Tag(models.Model):
    category = models.ForeignKey(Tag_Category, on_delete=models.CASCADE, verbose_name="标签")

    class Meta:
        db_table = "tb_tags"
        verbose_name = "标签"
        verbose_name_plural = verbose_name


class Question_Tag(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, verbose_name="问题id")
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE, verbose_name="标签id")

    class Meta:
        db_table = "tb_questions_tags"
        verbose_name = "标签"
        verbose_name_plural = verbose_name
