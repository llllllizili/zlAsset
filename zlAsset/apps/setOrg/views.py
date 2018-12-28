# -*- coding:utf-8 -*-
# Author: zili

from django.shortcuts import render,HttpResponse
from django.http import JsonResponse,HttpResponseRedirect
from urllib.parse import quote, unquote

# from django.core import serializers

from django.contrib.auth.decorators import login_required
# Create your views here.
import time,datetime
from .models import *
from .forms import *


@login_required(login_url='/login/')
def index(request):
    department_data =Department.objects.all()
    return render(request,'setOrg/department.html',{'department_data':department_data })
    # member_data = Member.objects.all()
    # return render(request,'setData/index.html',{'member_data':member_data })

#创建部门
@login_required(login_url='/login/')
def create_department(request):
    if request.method == 'POST':
        form = departmentForm(request.POST)
        if form.is_valid():
            #data = form.clean()
            name=form.cleaned_data['name']
            description=form.cleaned_data['description']
            val = Department.objects.filter(name=name)
            if not val:
                Department.objects.create(
                    name=name,
                    description=description,
                    )
                department_data =Department.objects.all()
                return render(request,'setOrg/department.html',{'department_data':department_data })
            else:
                error_data = name+'已存在'
                department_data =Department.objects.all()
                return render(request,'setOrg/department.html',{'department_data':department_data,'error_data':error_data})
        else:
            error = form.errors
            return render(request,'setOrg/department.html',{'form_error':error})
    else:
        return HttpResponseRedirect ('/setOrg/index/')

#获取部门
@login_required(login_url='/login/')
def get_department(request):
    department_data =Department.objects.all()
    return render(request,'setOrg/department.html',{'department_data':department_data })
#删除部门
@login_required(login_url='/login/')
def delete_department(request,id):
    val = Team.objects.filter(department_id=id)
    if val:
        error_data='请先删除相关团队和成员'
        department_data =Department.objects.all()
        return render(request,'setOrg/department.html',{'department_data':department_data,'error_data':error_data })
    else:
        Department.objects.filter(id=id).delete()
        department_data =Department.objects.all()
        return render(request,'setOrg/department.html',{'department_data':department_data })
#修改部门
@login_required(login_url='/login/')
def modify_department(request,id):
    department_data =Department.objects.get(id=id)
    return render(request,'setOrg/modify_department.html',{'department_data':department_data })
@login_required(login_url='/login/')
def modify_department_action(request):
    if request.method == 'POST':
        id=request.POST['id']
        name=request.POST['name']
        description=request.POST['description']
        Department.objects.filter(id=id).update(
                    name=name,
                    description=description,
                    )
        department_data =Department.objects.all()
        return render(request,'setOrg/department.html',{'department_data':department_data })
    else:
        return HttpResponseRedirect ('/setData/index/')