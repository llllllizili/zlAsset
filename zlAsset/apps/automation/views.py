# -*- coding:utf-8 -*-
# Author: zili

from django.shortcuts import render,HttpResponse
from urllib.parse import quote, unquote
from django.http import JsonResponse,HttpResponseRedirect
from django.contrib.auth.decorators import login_required
import time,datetime
import json
import base64
from .models import *

from .run_api import RunAutomation

@login_required(login_url='/login/')

def index(request):
    # return render(request,'automation/index.html',{'hdServer_data':hdServer_data})
    return render(request,'automation/index.html')

def add_job(request):
    return render(request,'automation/add_job.html')

