# -*- coding:utf-8 -*-
from __future__ import absolute_import
from celery import shared_task
#from celery.task import task


# import json
# from .sync_hddata import SyncHdInfo
# from .models import *
import time,datetime
from .views import os_data_sync

# operSyatem sync 
@shared_task
def osdata_sync():
    res = os_data_sync()
    return res
