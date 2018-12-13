# # -*- coding:utf-8 -*-
# from celery import Celery
# from celery.schedules import crontab

# broker = 'redis://:123qweASD@192.168.1.244:6379/1'
# backend = 'redis://:123qweASD@192.168.1.244:6379/2'

# app = Celery('tasks', broker=broker, backend=backend)

# @app.on_after_configure.connect
# def set_crontab_task(sender, **kwargs):
#     sender.add_periodic_task(3.0, test.s('hello'),name='add every 3s')
#     sender.add_periodic_task(5.0, test.s('world'), expires=10)
#     sender.add_periodic_task(
#         crontab(hour=7, minute=30, day_of_week=1),
#         test.s('Happy Mondays!'),
#     )

# #编写test函数.定时任务调用
# @app.task
# def crontab_test(args):
#     print args


# from celery import Celery
# from celery.schedules import crontab

# broker = 'redis://:123qweASD@192.168.1.244:6379/1'
# backend = 'redis://:123qweASD@192.168.1.244:6379/2'

# app = Celery('tasks', broker=broker, backend=backend)

# @app.task
# def send(message):
#     print message
#     return message


# app.conf.beat_schedule = {
#     'send-every-10-seconds': {
#         'task': 'crontab_tasks.send',
#         #'schedule': 3.0,
#         'schedule': crontab(minute='*/1'),
#         'args': ('Hello World',)
#     },
# }

# app.conf.timezone = 'UTC'