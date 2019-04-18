# -*- coding:utf-8 -*-
# Author: zili

from django.shortcuts import render,HttpResponse
from urllib.parse import quote, unquote
from django.http import JsonResponse,HttpResponseRedirect
from django.contrib.auth.decorators import login_required
import time,datetime
import json
import base64
import time,datetime
import string
import random

import logging
logger = logging.getLogger(__name__)

from .models import *

from .run_api import RunAutomation
from .run_api import script_path

from operSystem.models import Cert as osCert
from operSystem.models import Data as osData

@login_required(login_url='/login/')
def index(request):
    jobs_data =Jobs.objects.all()
    return render(request,'automation/index.html',{'jobs_data':jobs_data})

@login_required(login_url='/login/')
def add_job(request):
    try:
        cert_data=osCert.objects.all()
        #os_data=osData.objects.all()
        logger.info('/automation/add_job/')
        return render(request,'automation/add_job.html',{'cert_data':cert_data})
    except Exception  as e:
        logger.error('DB search error')
@login_required(login_url='/login/')
def add_job_action(request):
    if request.method == 'POST':
        name=request.POST['name']
        description=request.POST['description']
        language=request.POST['language']
        if language == 'python':
            postfix = '.py'
        if language == 'sh':
            postfix = '.sh'
        if language == 'batchfile':
            postfix = '.bat'
        if language == 'powershell':
            postfix = '.ps1'
        script_content=request.POST['script_content']
        job_script_path=script_path()+'automation/jobs/'
        # 随机11个字符串
        random_name = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(11))
        script_name = random_name+language+postfix
        create_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        user = request.user

        with open(job_script_path+script_name,'w+', encoding="utf-8") as f:
            script_content=script_content.replace('\r\n', '\n')
            f.writelines(script_content)

        job = Jobs.objects.filter(script_name=script_name)
        if not job:
            Jobs.objects.create(
                    name=name,
                    description=description,
                    script_name=script_name,
                    create_time=create_time,
                    user=user,
                    script_content=script_content
                    )
        else:
            Jobs.objects.filter(script_name=script_name).update(
                    name=name,
                    description=description,
                    create_time=create_time,
                    user=user,
                    script_content=script_content
            )
        jobs_data =Jobs.objects.all()
        return render(request,'automation/index.html',{'jobs_data':jobs_data})
    else:
        jobs_data =Jobs.objects.all()
        return render(request,'automation/index.html',{'jobs_data':jobs_data})


def test_job(request):
    if request.method == 'POST':
        name=request.POST['name']
        description=request.POST['description']
        language=request.POST['language']
        if language == 'python':
            postfix = '.py'
        if language == 'sh':
            postfix = '.sh'
        if language == 'batchfile':
            postfix = '.bat'
        if language == 'powershell':
            postfix = '.ps1'
        host=request.POST.getlist('host')

        script_content=request.POST['script_content']
        job_script_path=script_path()+'automation/jobs/test/'
         # 随机6个字符串
        random_name = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(6))
        script_name = random_name+language+postfix
        with open(job_script_path+script_name,'w+', encoding="utf-8") as f:
            script_content=script_content.replace('\r\n', '\n')
            f.writelines(script_content)

        res=list()
        for ip in host:
            cert_data=osCert.objects.get(ip=ip)
            test_conn=RunAutomation(
                ip = cert_data.ip,
                username = cert_data.username,
                password = bytes.decode(base64.b64decode(bytes(cert_data.password,encoding='utf-8'))),
                os_type = cert_data.os_type,
                port=cert_data.port
                )
            jobs_data = test_conn.test_job(script_name)
            jobs_data['ip'] =ip
            res.append(jobs_data)
        #删除测试生成的脚本,可能会遇到权限问题
        import os
        delete_test_script='rm -rf '+job_script_path+script_name
        os.system(delete_test_script)
        return render(request,'automation/test_job.html',{
            'res':res,
        })
    else:
        jobs_data =Jobs.objects.all()
        return render(request,'automation/index.html',{'jobs_data':jobs_data})

def delete_job(request,id):
    Jobs.objects.filter(id=id).delete()
    jobs_data =Jobs.objects.all()
    return render(request,'automation/index.html',{'jobs_data':jobs_data})

# 暂不写.读取内容无法渲染到前端ace
def modify_job(request,id):
    jobs_data =Jobs.objects.all()
    return render(request,'automation/index.html',{'jobs_data':jobs_data})

def job_detail(request,id):
    jobs_data =Jobs.objects.get(id=id)
    script_content=jobs_data.script_content
    return render(request,'automation/job_detail.html',{'jobs_data':jobs_data})
