# -*- coding:utf-8 -*-
from django.shortcuts import render,redirect,HttpResponse


from functools import wraps

from users.models import User
# 说明：这个装饰器的作用在每个视图函数被调用时，都验证下有没法有登录，
# 如果有过登录，则可以执行新的视图函数，否则没有登录则自动跳转到登录页面
# 前提开启session,django默认开启session
def check_login(f):
    @wraps(f)
    def inner(request,*arg,**kwargs):
        if request.session.get('is_login')=='1':
            return f(request,*arg,**kwargs)
        else:
            return redirect('/login/')
    return inner


@check_login
def index(request):
    return render(request, 'index/index.html')

from .forms import loginForm

def login(request):

    if request.method=="POST":

        form = loginForm(request.POST) # 提交过来的数据
        if form.is_valid():# 如果提交的数据合法
            # data = form.clean()    　　#.clen()获取提交的数据
            # username = data['username']

            #
            username=form.cleaned_data['username']
            password=form.cleaned_data['password']
        # username=request.POST.get('username') #get可设置默认值
        # password=request.POST.get('password')
        # print(username)
        # print(password)
            user=User.objects.filter(username=username,password=password)

            if user:
            #登录成功
            # 1，生成特殊字符串
            # 2，这个字符串当成key，此key在数据库的session表（在数据库存中一个表名是session的表）中对应一个value
            # 3，在响应中,用cookies保存这个key ,(即向浏览器写一个cookie,此cookies的值即是这个key特殊字符）
                request.session['is_login']='1'
                # 这个session是用于后面访问每个页面（即调用每个视图函数时要用到，即判断是否已经登录，用此判断）
                # request.session['username']=username  # 这个要存储的session是用于后面，每个页面上要显示出来，登录状态的用户名用。
                # 说明：如果需要在页面上显示出来的用户信息太多（有时还有积分，姓名，年龄等信息），所以我们可以只用session保存user_id
                request.session['user_id']=user[0].id
                return render(request,'index/index.html')
                #return render(request,'index/index.html',{"username":user[0]})
            else:
                return render(request,'common/login.html',{'login_status':'用户名或密码错误'})
        else:
            error = form.errors
            print(type(form.errors),form.errors)
            return render(request,'common/login.html',{'form_error':error})
    else:
        # 如果是GET请求，就说明是用户刚开始登录，使用URL直接进入登录页面的
        return render(request,'common/login.html')


def logout(request):
    #注销
    request.session.clear()
    pass
