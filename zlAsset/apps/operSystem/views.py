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
import ast
import time,datetime
import json
from .models import *
from .sync_osdata import GetSysDataL

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
    # os_data=Data.objects.get(id=id)
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
    return render(request,'operSystem/index.html',{'operSystem_data':operSystem_data})

# 修改
@login_required(login_url='/login/')
def modify_os(request,id):
    operSystem_data =Data.objects.get(id=id)
    return render(request,'operSystem/modify_os.html',{'operSystem_data':operSystem_data})
@login_required(login_url='/login/')
def modify_os_action(request):
    if request.method == 'POST':
        id=request.POST['id']
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
        hdserver_data = hdData.objects.get(id=hdserver_id)

        # hd_data=Data.objects.get(id=id)
        # cert = Cert.objects.filter(hd_name=hd_data.name)
        # if cert:
        #     Cert.objects.filter(hd_name=hd_data.name).update(hd_name=name)

        Data.objects.filter(id=id).update(
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
        return render(request,'operSystem/index.html',{'operSystem_data':operSystem_data })
    else:
        return HttpResponseRedirect ('/operSystem/index/')

@login_required(login_url='/login/')
def base_detail(request,id):
    operSystem_data =Data.objects.get(id=id)
    return render(request,'operSystem/base_detail.html',{'operSystem_data':operSystem_data})

@login_required(login_url='/login/')
def sync_detail(request,id):
    operSystem_data =Data.objects.get(id=id)

    cert = Cert.objects.filter(os_host_ip=operSystem_data.host_ip)
    if cert:
        Cert_data = Cert.objects.get(os_host_ip=operSystem_data.host_ip)
        if SyncData.objects.filter(cert_ip=Cert_data.ip):
            sync_data = SyncData.objects.get(cert_ip=Cert_data.ip)
            cpu_model=ast.literal_eval(sync_data.cpu_model)
            disk_data=ast.literal_eval(sync_data.logicdisk)
            network_data=ast.literal_eval(sync_data.network)
        else:
            sync_data=None
    else:
        Cert_data = None
        sync_data = None
    return render(request,'operSystem/sync_detail.html',{
        'operSystem_data':operSystem_data,
        'Cert_data':Cert_data,
        'sync_data':sync_data,
        'cpu_model':cpu_model,
        'disk_data':disk_data,
        'network_data':network_data
        })




@login_required(login_url='/login/')
def set_cert(request,id):
     if request.method == 'POST':
        ip=request.POST['ip']
        os_type=request.POST['os_type']
        username=request.POST['username']
        password=request.POST['password']

        operSystem_data =Data.objects.get(id=id)
        val = Cert.objects.filter(os_host_ip=operSystem_data.host_ip)
        if not val:
            Cert.objects.create(
                os_host_ip=operSystem_data.host_ip,
                ip=ip,
                port=port,
                os_type=os_type,
                username=username,
                password=password,
                sync='on'
                )
        else:
            Cert.objects.filter(os_host_ip=operSystem_data.host_ip).update(
                os_host_ip=operSystem_data.host_ip,
                ip=ip,
                port=port,
                os_type=os_type,
                username=username,
                password=password,
                sync='on'
            )

        return HttpResponseRedirect ("/operSystem/sync_detail/"+str(id))

def set_sync(request,id):
    operSystem_data =Data.objects.get(id=id)
    os_host_ip=operSystem_data.host_ip

    if request.method == 'POST':
        val = Cert.objects.get(os_host_ip=os_host_ip)
        sync = val.sync
        if sync == 'on':
            sync = 'off'
        else:
            sync = 'on'
            os_type = val.os_type

            if os_type=='windows':
                pass
            if os_type=='linux':
                sync_login=GetSysDataL(
                    ip=val.ip,
                    port=val.port,
                    username=val.username,
                    password=val.password,
                    os_type=val.os_type,
                    )
                sync_info=sync_login.get_os_info()

                update_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

                sync_data = SyncData.objects.filter(cert_ip=val.ip)

                sync_info_dict = json.loads(sync_info[val.ip]['script'])
                #print(sync_info_dict)

                if not sync_data:
                    SyncData.objects.create(
                        cert_ip=val.ip,
                        host_ip=val.ip,
                        hostname=sync_info_dict['hostname'],
                        os_sys=sync_info_dict['os_sys'],
                        os_version=sync_info_dict['os_version'],
                        os_kernel=sync_info_dict['os_kernel'],
                        cpu_model=sync_info_dict['cpu_model'],
                        cpu_num=sync_info_dict['cpu_num'],
                        cpu_core=sync_info_dict['cpu_core'],
                        mem_total=sync_info_dict['mem_total'],
                        disk_total=sync_info_dict['disk_total'],
                        product_id=sync_info_dict['product_id'],
                        #phydisk=sync_info_dict['phydisk'],
                        logicdisk=sync_info_dict['logicdisk'],
                        install_date=sync_info_dict['install_date'],
                        network=sync_info_dict['network'],
                        update_time=update_time
                    )
                else:
                    SyncData.objects.filter(cert_ip=val.ip).update(
                        host_ip=val.ip,
                        hostname=sync_info_dict['hostname'],
                        os_sys=sync_info_dict['os_sys'],
                        os_version=sync_info_dict['os_version'],
                        os_kernel=sync_info_dict['os_kernel'],
                        cpu_model=sync_info_dict['cpu_model'],
                        cpu_num=sync_info_dict['cpu_num'],
                        cpu_core=sync_info_dict['cpu_core'],
                        mem_total=sync_info_dict['mem_total'],
                        disk_total=sync_info_dict['disk_total'],
                        product_id=sync_info_dict['product_id'],
                        #phydisk=sync_info_dict['phydisk'],
                        logicdisk=sync_info_dict['logicdisk'],
                        install_date=sync_info_dict['install_date'],
                        network=sync_info_dict['network'],
                        update_time=update_time
                        )

        Cert.objects.filter(os_host_ip=os_host_ip).update(sync=sync)
    else:
        pass
    return HttpResponseRedirect ("/operSystem/sync_detail/"+str(id))