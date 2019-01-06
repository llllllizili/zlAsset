# -*- coding:utf-8 -*-
from __future__ import absolute_import
from celery import shared_task
#from celery.task import task


# import json
# from .sync_hddata import SyncHdInfo
# from .models import *
import time,datetime
from .views import hd_data_sync

@shared_task
def add(x,y):
    time.sleep(10)
    return int(x)+int(y)

# #hdServer sync ipmi info
@shared_task
def ipmi_sync():
    res = hd_data_sync()
    return res
