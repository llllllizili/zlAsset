# -*- coding:utf-8 -*-
from django.shortcuts import render,HttpResponse
from urllib.parse import quote, unquote


# Create your views here.
import time
import json
from .hddata import SyncHdInfo


def get_hd_info(request):
    '''
    username=
    password=
    server=
    '''

    ilo_login = SyncHdInfo(username='administrator',password='123qweASD',server='192.168.3.11')
    ilo_info = ilo_login.get_hd_info_ilo()

    return render(request, 'hdServer/return_value.html', {'return_value': ilo_info})

def task_add_test(request):
    x = request.GET['x']
    y = request.GET['y']

    from .tasks import add
    #delay函数实现异步
    result = add.delay(x,y)
    res = {'code':200, 'message':'ok', 'data':[{'x':x, 'y':y}]}
    return render(request, 'hdServer/return_value.html', {'return_value': json.dumps(res)})
#     #result.ready()     #判断任务是否完成处理 True 或 False
#     #result.get(timeout=1)  # 可以重新抛出异常
#     #result.traceback   #可以获取原始的回溯信息
