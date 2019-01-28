# -*- coding:utf-8 -*-
# Author: zili


from django.shortcuts import render,HttpResponse
from urllib.parse import quote, unquote
from django.http import JsonResponse,HttpResponseRedirect

from .sync_osdata import GetSysDataL
# FBV(function base views) 登录校验
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password, check_password
#from django.db.models import Q
# Create your views here.
import os
import time,datetime
import json
from .models import *


import sys
sys.path.append("../")
from hdServer.models import Data as hdData


def test(request):
    run = GetSysDataL(ip='192.168.1.55',username='root',password='centos',port=22,os_type='linux')
    #os_data = run.cmd_test()


    script_data = run.script_test()


    return render(request,'operSystem/return_value.html',{'os_data':script_data})



@login_required(login_url='/login/')
def index(request):
    operSystem_data =Data.objects.all()

    return render(request,'operSystem/index.html',{'operSystem_data':operSystem_data})

@login_required(login_url='/login/')
def add_os(request):
    return render(request, 'operSystem/add_os.html')

@login_required(login_url='/login/')
def add_os_action(request):
    if request.method == 'POST':
        hostname=request.POST.get('hostname','未填写')
        host_ip=request.POST['host_ip']
        description=request.POST['description']
        hdserver_id=request.POST['hdserver_id']
        department=request.POST['department']
        team=request.POST['team']
        use_member=request.POST['use_member']
        start_date=request.POST['start_date']
        end_date=request.POST['end_date']
        run_env=request.POST['run_env']
        os_data = Data.objects.filter(host_ip=host_ip)
        hdserver_data = hdData.objects.get(id=hdserver_id)
        if not os_data:
            Data.objects.create(
                hostname=hostname,
                host_ip=host_ip,
                description=description,
                hdserver_id=hdserver_id,
                hdserver_name=hdserver_data.name,
                department=department,
                team=team,
                use_member=use_member,
                start_date=start_date,
                end_date=end_date,
                run_env=run_env,
                )
            operSystem_data =Data.objects.all()
            return render(request,'operSystem/index.html',{'operSystem_data':operSystem_data})
        else:
            error_data = host_ip +'已存在'
            operSystem_data =Data.objects.all()
            return render(request,'operSystem/index.html',{'operSystem_data':operSystem_data,'error_data':error_data})
    else:
        return HttpResponseRedirect ('/operSystem/index/')

@login_required(login_url='/login/')
def delete_os(request,id):
    os_data=Data.objects.get(id=id)
    # cert=Cert.objects.filter(hd_name=os_data.name)
    # if cert:
    #     cert_data=Cert.objects.get(hd_name=os_data.name)
    #     if cert_data.way=='ipmi':
    #         IpmiData.objects.filter(cert_ip=cert_data.ip).delete()
    #     if cert_data.way=='ilo':
    #         IloData.objects.filter(cert_ip=cert_data.ip).delete()
    #     Cert.objects.filter(hd_name=os_data.name).delete()
    Data.objects.filter(id=id).delete()
    operSystem_data =Data.objects.all()
    return render(request,'hdServer/index.html',{'operSystem_data':operSystem_data})
