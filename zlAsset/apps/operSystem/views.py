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

def test(request):
    run = GetSysDataL(ip='192.168.1.55',username='root',password='centos',port=22,os_type='linux')
    #os_data = run.cmd_test()


    script_data = run.script_test()


    return render(request,'operSystem/return_value.html',{'os_data':script_data})
