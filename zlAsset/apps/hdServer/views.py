# -*- coding:utf-8 -*-
from django.shortcuts import render,HttpResponse
from urllib.parse import quote, unquote

# FBV(function base views) 登录校验
from django.contrib.auth.decorators import login_required

# Create your views here.
import time
import json
from .sync_hddata import SyncHdInfo
from .models import *

@login_required(login_url='/login/')
def test(request):
    test = 'this is hdServer test'
    return render(request, 'hdServer/test.html', {'test': test})


@login_required(login_url='/login/')
def index(request):
    return render(request, 'hdServer/index.html')

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

#添加服务器
def add_hd(request):
    # if request.method == 'POST':
    #     id=request.POST['id']
    test='test'
    return render(request, 'hdServer/add_hd.html')
def add_hd_action(request):
    if request.method == 'POST':
        name=request.POST.get('name','未填写')
        brand=request.POST['brand']
        brand_type=request.POST['brand_type']
        run_env=request.POST['run_env']
        manager_ip=request.POST['manager_ip']
        device_ip=request.POST['device_ip']
        description=request.POST['description']
        oper_member=request.POST['oper_member']
        department=request.POST['department']
        team=request.POST['team']
        use_member=request.POST['use_member']
        position=request.POST['position']
        datacenter=request.POST['datacenter']
        cabinet=request.POST['cabinet']
        u_num=request.POST['u_num']
        u_start=request.POST['u_start']
        u_end=request.POST['u_end']
        asset_num=request.POST['asset_num']
        asset_sn=request.POST['asset_sn']
        support_start=request.POST['support_start']
        support_end=request.POST['support_end']
        hd_cost=request.POST['hd_cost']
        supplier=request.POST['supplier']

        val = Data.objects.filter(name=name)
        if not val:
            Data.objects.create(
                name=name,
                brand=brand,
                brand_type=brand_type,
                run_env=brand_type,
                manager_ip=manager_ip,
                device_ip=device_ip,
                description=description,
                oper_member=oper_member,
                department=department,
                team=team,
                use_member=use_member,
                position=position,
                datacenter=datacenter,
                cabinet=cabinet,
                u_num=u_num,
                u_start=u_start,
                u_end=u_end,
                asset_num=asset_num,
                asset_sn=asset_sn,
                support_start=support_start,
                support_end=support_end,
                hd_cost=hd_cost,
                supplier=supplier,
                )
            hdServer_data =Data.objects.all()
            return render(request,'hdServer/index.html',{'hdServer_data':hdServer_data })
        else:
            error_data = name+'已存在'
            hdServer_data =Department.objects.all()
            return render(request,'hdServer/index.html',{'hdServer_data':hdServer_data,'error_data':error_data})
    else:
        # return HttpResponseRedirect ('/hdServer/')
        pass
