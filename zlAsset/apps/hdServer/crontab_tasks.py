# # -*- coding:utf-8 -*-
from celery import Celery
from celery.schedules import crontab

app = Celery('crontab_tasks', broker='redis://:123qweASD@192.168.1.244:6379/1')


@app.task
def send(message):
    return message


app.conf.beat_schedule = {
    'send-every-10-seconds': {
        'task': 'crontab_tasks.send',
        'schedule': 10.0,
        'args': ('Hello World', )
    }
}
