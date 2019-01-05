# -*- coding:utf-8 -*-

from __future__ import absolute_import
import os
from celery import Celery
from django.conf import settings

#这里我们的项目名称为,所以为platform.settings
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "zlAsset.settings")
#创建celery 应用
app = Celery('zlAsset')

app.config_from_object('django.conf:settings')

app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))  #dumps its own request information



#定时任务 #成功
from celery.schedules import crontab
from datetime import timedelta

app.conf.update(
    CELERYBEAT_SCHEDULE = {
        # 周期任务. 两种方式
        # 一小时一次
        'sum-task': {
            'task': 'hdServer.tasks.add', #应用下的tasks
            'schedule':  timedelta(seconds=5),
            'args': (3000, 600)
        },
        # 2h 一次
        'task-one': {
            'task': 'hdServer.tasks.add',
            'schedule': 7200.0, # 每5秒执行一次
            'args': (7000,200)
        }
    }
)
