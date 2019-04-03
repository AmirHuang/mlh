# _*_ coding: utf-8 _*_
# @time     : 2019/04/02
# @Author   : Amir
# @Site     : 
# @File     : main.py
# @Software : PyCharm


from celery import Celery
# 为celery使用django配置文件进行设置
import os


if not os.getenv('DJANGO_SETTINGS_MODULE'):
    os.environ['DJANGO_SETTINGS_MODULE'] = 'mlh.settings'
# 创建celery应用
app = Celery('celery_tasks')
# 导入celery配置
app.config_from_object('celery_tasks.config')
# 自动注册celery任务
app.autodiscover_tasks(['celery_tasks.sms'])

# 启动ｃｅｌｅｒｙ应用
#  celery -A celery_tasks.main worker -l info
