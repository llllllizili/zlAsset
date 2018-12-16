# -*- coding:utf-8 -*-
from django.shortcuts import render,redirect,HttpResponse
# Django 认证系统
from django.contrib import auth
from django.contrib.auth.models import User
# FBV(function base views) 登录校验
from django.contrib.auth.decorators import login_required
# CBV 登录校验
# from django.utils.decorators import method_decorator

from .forms import loginForm

@login_required(login_url='/login/')
def index(request):
    return render(request, 'index/index.html')


def login(request):
    if request.method == 'POST':
        form = loginForm(request.POST) # 提交过来的数据
        if form.is_valid(): # 如果提交的数据合法
            data = form.clean() #.clean()获取提交的数据
            username=form.cleaned_data['username']
            password=form.cleaned_data['password']
            user = auth.authenticate(username=username, password=password)

            #设置session中username
            request.session['username']=username
            #request.session['user_id']=user[0].id
            if user:
                auth.login(request, user)
                return render(request,'index/index.html')
            else:
                return render(request,'common/login.html',{'login_status':'用户名或密码错误'})
        else:
            error = form.errors
            return render(request,'common/login.html',{'form_error':error})
    return render(request,'common/login.html')

# def register(request):
#     if request.method == 'GET':
#         return render(request, 'register.html')
#     if request.method == 'POST':
#         username = request.POST.get('username')
#         password = request.POST.get('password')
#         email = request.POST.get('email')
#         user = authenticate(username=username, password=password)  # 判断用户是否存在
#         if user:
#             return render(request, 'register.html')
#         User.objects.create_user(name, email, password)  # 创建用户保存在auth_user表中
#         return render(request,'index/index.html')  # 跳转到登录页面

def logout(self):
    def log_out(request):
        auth.logout(request)
        #return render(request,'common/login.html')
