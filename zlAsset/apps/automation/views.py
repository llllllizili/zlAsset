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
    logger.info("一个更萌的请求过来了。。。。")
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
        job_script_path=script_path()+'automation/jobs/test/'
        # 随机22个字符串
        random_name = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(22))
        script_name = random_name+language+postfix
        create_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        user = request.user

        with open(job_script_path+script_name,'w+') as f:
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
    print('tttttttttttttttttttt=================')
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

        print(name)
        print(description)
        print(language)
        print(host)


        script_content=request.POST['script_content']
        job_script_path=script_path()+'automation/jobs/test/'
         # 随机22个字符串
        random_name = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(22))
        script_name = random_name+language+postfix

        with open(job_script_path+script_name,'w+') as f:
            f.writelines(script_content)
        return render(request,'automation/test_job.html',{
            'job_name':name,
            'job_description':description,
            'job_script_content':script_content,
            'job_script_name':script_name
        })
    else:
        jobs_data =Jobs.objects.all()
        return render(request,'automation/index.html',{'jobs_data':jobs_data})

# def test_job_save(request):
#     if request.method == 'POST':
#         name=request.POST['name']
#         description=request.POST['description']
#         script_content=request.POST['script_content']
#         script_name=request.POST['script_name']
#         create_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
#         user = request.user

#         job_script_path=script_path()+'automation/jobs/'

#         with open(job_script_path+script_name,'w+') as f:
#             f.writelines(script_content)

#         job = Jobs.objects.filter(script_name=script_name)
#         if not job:
#             Jobs.objects.create(
#                     name=name,
#                     description=description,
#                     script_name=script_name,
#                     create_time=create_time,
#                     user=user,
#                     script_content=script_content
#                     )
#         else:
#             Jobs.objects.filter(script_name=script_name).update(
#                     name=name,
#                     description=description,
#                     create_time=create_time,
#                     user=user,
#                     script_content=script_content
#             )
#         jobs_data =Jobs.objects.all()
#         return render(request,'automation/index.html',{'jobs_data':jobs_data})
#     else:
#         jobs_data =Jobs.objects.all()
#         return render(request,'automation/index.html',{'jobs_data':jobs_data})

# def test_job_action(request):
#     if request.method == 'POST':
#         name=request.POST['name']
#         description=request.POST['description']
#         script_content=request.POST['script_content']
#         script_name=request.POST['script_name']
#         create_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
#         user = request.user

#         job_script_path=script_path()+'automation/jobs/'

#         with open(job_script_path+script_name,'w+') as f:
#             f.writelines(script_content)

#         job = Jobs.objects.filter(script_name=script_name)
#         if not job:
#             Jobs.objects.create(
#                     name=name,
#                     description=description,
#                     script_name=script_name,
#                     create_time=create_time,
#                     user=user
#                     )
#             jobs_data =Jobs.objects.all()
#         else:
#             Jobs.objects.filter(script_name=script_name).update(
#                     name=name,
#                     description=description,
#                     create_time=create_time,
#                     user=user
#             )
#         jobs_data =Jobs.objects.all()
#         return render(request,'automation/index.html',{'jobs_data':jobs_data})
#     else:
#         jobs_data =Jobs.objects.all()
#         return render(request,'automation/index.html',{'jobs_data':jobs_data})

def delete_job(request,id):
    jobs_data =Jobs.objects.all()
    return render(request,'automation/index.html',{'jobs_data':jobs_data})

def modify_job(request,id):
    jobs_data =Jobs.objects.all()
    return render(request,'automation/index.html',{'jobs_data':jobs_data})

def job_detail(request,id):
    jobs_data =Jobs.objects.get(id=id)
    script_content=jobs_data.script_content
    return render(request,'automation/job_detail.html',{'jobs_data':jobs_data})
