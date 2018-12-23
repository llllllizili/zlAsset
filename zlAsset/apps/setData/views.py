from django.shortcuts import render,HttpResponse
from django.http import JsonResponse
from urllib.parse import quote, unquote

# from django.core import serializers

from django.contrib.auth.decorators import login_required
# Create your views here.
import time,datetime
from .models import *
from .forms import *

@login_required(login_url='/login/')
def index(request):
    brand_data = Brand.objects.all()
    return render(request,'setData/index.html',{'brand_data':brand_data })
    #return render(request,'setData/index.html')

#新加品牌
@login_required(login_url='/login/')
def create_brand(request):
    if request.method == 'POST':
        form = brandForm(request.POST)
        if form.is_valid():
            #data = form.clean()
            name=form.cleaned_data['name']
            val = Brand.objects.filter(name=name)
            if not val:
                dtime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                #un_time = time.mktime(dtime.timetuple())

                Brand.objects.create(
                    name=name,
                    create_time=dtime,
                    who_create=request.user.username
                    )
                brand_data =Brand.objects.all()
                return render(request,'setData/index.html',{'brand_data':brand_data })
            else:
                error_data = name+'已存在'
                brand_data =Brand.objects.all()
                return render(request,'setData/index.html',{'brand_data':brand_data,'error_data':error_data})
        else:
            error = form.errors
            return render(request,'setData/index.html',{'form_error':error})
    else:
        return HttpResponse ('create_brand 不支持GET请求')
#获取品牌
@login_required(login_url='/login/')
def get_brand(request):
    #brand_data =serializers.serialize("json", Brand.objects.all())
    brand_data =Brand.objects.all()
    return render(request,'setData/index.html',{'brand_data':brand_data })
#修改品牌
@login_required(login_url='/login/')
def modify_brand(request,id):
    brand_data =Brand.objects.get(id=id)
    return render(request,'setData/modify_brand.html',{'brand_data':brand_data })
@login_required(login_url='/login/')
def modify_brand_action(request):
    if request.method == 'POST':
        id=request.POST['id']
        brand=request.POST['brand']
        dtime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        Brand.objects.filter(id=id).update(
                    name=brand,
                    create_time=dtime,
                    who_create=request.user.username
                    )
        brand_data =Brand.objects.all()
        return render(request,'setData/index.html',{'brand_data':brand_data })
    else:
        return HttpResponse ('modify_brand_action 不支持GET请求')
#删除品牌
@login_required(login_url='/login/')
def delete_brand(request,id):
    #id = request.GET['id']
    #id = request.GET.get('id', '')
    Brand.objects.filter(id=id).delete()
    brand_data =Brand.objects.all()
    return render(request,'setData/index.html',{'brand_data':brand_data })


#新加型号
@login_required(login_url='/login/')
def create_brandtype(request):
    if request.method == 'POST':
        form = brandtypeForm(request.POST)
        if form.is_valid():
            #data = form.clean()
            brand=form.cleaned_data['brand']
            brandtype=form.cleaned_data['brandtype']

            val = BrandType.objects.filter(name=brandtype,brand_name=brand)
            brabd_info =Brand.objects.get(name=brand)
            if not val:
                dtime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                #un_time = time.mktime(dtime.timetuple())
                BrandType.objects.create(
                    name=brandtype,
                    brand_name=brand,
                    create_time=dtime,
                    who_create=request.user.username,
                    brand_id=brabd_info.id
                    )
                brandtype_data = BrandType.objects.all()
                return render(request,'setData/brandtype.html',{'brandtype_data':brandtype_data })

            else:
                error_data = brand+'--'+brandtype+'已存在'
                brandtype_data = BrandType.objects.all()
                return render(request,'setData/brandtype.html',{'brandtype_data':brandtype_data,'error_data':error_data})
        else:
            error = form.errors
            return render(request,'setData/brandtype.html',{'form_error':error})
    else:
        return HttpResponse ('create_brandtype 不支持GET请求')
#获取型号
@login_required(login_url='/login/')
def get_brandtype(request):
    brandtype_data = BrandType.objects.all()
    return render(request,'setData/brandtype.html',{'brandtype_data':brandtype_data })
#修改型号
@login_required(login_url='/login/')
def modify_brandtype(request,id):
    brandtype_data =BrandType.objects.get(id=id)
    return render(request,'setData/modify_brandtype.html',{'brandtype_data':brandtype_data })
@login_required(login_url='/login/')
def modify_brandtype_action(request):
    if request.method == 'POST':
        id=int(request.POST['id'])
        brand=request.POST['brand']
        brandtype=request.POST['brandtype']

        dtime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        BrandType.objects.filter(id=id).update(
                    name=brandtype,
                    brand_name=brand,
                    create_time=dtime,
                    who_create=request.user.username
                    )
        brandtype_data =BrandType.objects.all()
        return render(request,'setData/brandtype.html',{'brandtype_data':brandtype_data })
    else:
        return HttpResponse ('modify_brandtype_action 不支持GET请求')

#删除型号
@login_required(login_url='/login/')
def delete_brandtype(request,id):
    BrandType.objects.filter(id=id).delete()
    brandtype_data =BrandType.objects.all()
    return render(request,'setData/brandtype.html',{'brandtype_data':brandtype_data })
