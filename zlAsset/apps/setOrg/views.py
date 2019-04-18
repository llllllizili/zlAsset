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
    # department_data =Department.objects.all()
    # return render(request,'setOrg/department.html',{'department_data':department_data })
    member_data = Member.objects.all()
    return render(request,'setOrg/index.html',{'member_data':member_data })

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



#创建团队
@login_required(login_url='/login/')
def create_team(request):
    if request.method == 'POST':
        form = teamForm(request.POST)
        if form.is_valid():
            #data = form.clean()
            name=form.cleaned_data['name']
            description=form.cleaned_data['description']
            department=form.cleaned_data['department']
            val = Team.objects.filter(name=name)
            department_info =Department.objects.get(name=department)
            if not val:
                Team.objects.create(
                    name=name,
                    description=description,
                    department_name=department,
                    department_id=department_info.id,
                    )
                team_data =Team.objects.all()
                return render(request,'setOrg/team.html',{'team_data':team_data })
            else:
                error_data = name+'已存在'
                team_data =Team.objects.all()
                return render(request,'setOrg/team.html',{'team_data':team_data,'error_data':error_data})
        else:
            error = form.errors
            return render(request,'setOrg/team.html',{'form_error':error})
    else:
        return HttpResponseRedirect ('/setOrg/index/')
#获取团队
@login_required(login_url='/login/')
def get_team(request):
    team_data =Team.objects.all()
    return render(request,'setOrg/team.html',{'team_data':team_data })
#删除团队
@login_required(login_url='/login/')
def delete_team(request,id):
    val = Member.objects.filter(team_id=id)
    if val:
        error_data='请先删除相关团队和成员'
        team_data =Team.objects.all()
        return render(request,'setOrg/team.html',{'team_data':team_data,'error_data':error_data })
    else:
        Team.objects.filter(id=id).delete()
        team_data =Team.objects.all()
        return render(request,'setOrg/team.html',{'team_data':team_data })
#修改团队
@login_required(login_url='/login/')
def modify_team(request,id):
    team_data =Team.objects.get(id=id)
    return render(request,'setOrg/modify_team.html',{'team_data':team_data })
@login_required(login_url='/login/')
def modify_team_action(request):
    if request.method == 'POST':
        id=request.POST['id']
        name=request.POST['name']
        description=request.POST['description']
        department=request.POST['department']

        department_info =Department.objects.get(name=department)
        Team.objects.filter(id=id).update(
                    name=name,
                    description=description,
                    department_name=department,
                    department_id=department_info.id,
                    )
        team_data =Team.objects.all()
        return render(request,'setOrg/team.html',{'team_data':team_data })
    else:
        return HttpResponseRedirect ('/setData/index/')



#创建成员
@login_required(login_url='/login/')
def create_member(request):
    if request.method == 'POST':
        form = memberForm(request.POST)
        if form.is_valid():
            name=form.cleaned_data['name']
            team=form.cleaned_data['team']
            phone=form.cleaned_data['phone']
            email=form.cleaned_data['email']

            val = Member.objects.filter(name=name)
            team_info =Team.objects.get(name=team)
            if not val:
                Member.objects.create(
                    name=name,
                    team_name=team,
                    phone=phone,
                    email=email,
                    team_id=team_info.id,
                    )
                member_data =Member.objects.all()
                return render(request,'setOrg/index.html',{'member_data':member_data })
            else:
                error_data = name+'已存在'
                member_data =Member.objects.all()
                return render(request,'setOrg/index.html',{'member_data':member_data,'error_data':error_data})
        else:
            error = form.errors
            return render(request,'setOrg/index.html',{'form_error':error})
    else:
        return HttpResponseRedirect ('/setOrg/index/')

#获取成员
@login_required(login_url='/login/')
def get_member(request):
    member_data =Member.objects.all()
    return render(request,'setOrg/index.html',{'member_data':member_data })

#删除成员
@login_required(login_url='/login/')
def delete_member(request,id):
    Member.objects.filter(id=id).delete()
    member_data =Member.objects.all()
    return render(request,'setOrg/index.html',{'member_data':member_data })

#修改成员
@login_required(login_url='/login/')
def modify_member(request,id):
    member_data =Member.objects.get(id=id)
    return render(request,'setOrg/modify_member.html',{'member_data':member_data })
@login_required(login_url='/login/')
def modify_member_action(request):
    if request.method == 'POST':
        id=request.POST['id']
        name=request.POST['name']
        team_name=request.POST['team']
        phone=request.POST['phone']
        email=request.POST['email']

        team_info =Team.objects.get(name=team_name)
        Member.objects.filter(id=id).update(
                    name=name,
                    team_name=team_name,
                    phone=phone,
                    email=email,
                    team_id=team_info.id,
                    )
        member_data =Member.objects.all()
        return render(request,'setOrg/index.html',{'member_data':member_data })
    else:
        return HttpResponseRedirect ('/setData/index/')
`