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
from .models import *

from .run_api import RunAutomation
from .run_api import script_path


@login_required(login_url='/login/')
def index(request):
    jobs_data =Jobs.objects.all()
    return render(request,'automation/index.html',{'jobs_data':jobs_data})

@login_required(login_url='/login/')
def add_job(request):
    return render(request,'automation/add_job.html')

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
                    user=user
                    )
        else:
            Jobs.objects.filter(script_name=script_name).update(
                    name=name,
                    description=description,
                    create_time=create_time,
                    user=user
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
            'job_script_content':str(script_content),
            'job_script_name':script_name
        })
    else:
        jobs_data =Jobs.objects.all()
        return render(request,'automation/index.html',{'jobs_data':jobs_data})

def test_job_save(request):
    if request.method == 'POST':
        name=request.POST['name']
        description=request.POST['description']
        script_content=request.POST['script_content']
        script_name=request.POST['script_name']
        create_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        user = request.user

        job_script_path=script_path()+'automation/jobs/'

        with open(job_script_path+script_name,'w+') as f:
            f.writelines(script_content)

        job = Jobs.objects.filter(script_name=script_name)
        if not job:
            Jobs.objects.create(
                    name=name,
                    description=description,
                    script_name=script_name,
                    create_time=create_time,
                    user=user
                    )
        else:
            Jobs.objects.filter(script_name=script_name).update(
                    name=name,
                    description=description,
                    create_time=create_time,
                    user=user
            )
        jobs_data =Jobs.objects.all()
        return render(request,'automation/index.html',{'jobs_data':jobs_data})
    else:
        jobs_data =Jobs.objects.all()
        return render(request,'automation/index.html',{'jobs_data':jobs_data})

def test_job_action(request):
    if request.method == 'POST':
        name=request.POST['name']
        description=request.POST['description']
        script_content=request.POST['script_content']
        script_name=request.POST['script_name']
        create_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        user = request.user

        job_script_path=script_path()+'automation/jobs/'

        with open(job_script_path+script_name,'w+') as f:
            f.writelines(script_content)

        job = Jobs.objects.filter(script_name=script_name)
        if not job:
            Jobs.objects.create(
                    name=name,
                    description=description,
                    script_name=script_name,
                    create_time=create_time,
                    user=user
                    )
            jobs_data =Jobs.objects.all()
        else:
            Jobs.objects.filter(script_name=script_name).update(
                    name=name,
                    description=description,
                    create_time=create_time,
                    user=user
            )
        jobs_data =Jobs.objects.all()
        return render(request,'automation/index.html',{'jobs_data':jobs_data})
    else:
        jobs_data =Jobs.objects.all()
        return render(request,'automation/index.html',{'jobs_data':jobs_data})
