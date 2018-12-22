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
            else:
                dtime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                #un_time = time.mktime(dtime.timetuple())

                Brand.objects.filter(name=name).update(
                    name=name,
                    create_time=dtime,
                    who_create=request.user.username
                    )
            brand_data =Brand.objects.all()
            return render(request,'setData/index.html',{'brand_data':brand_data })
        else:
            error = form.errors
            return render(request,'setData/index.html',{'form_error':error})
    else:
        return HttpResponse ('不支持GET请求')

#查找品牌
@login_required(login_url='/login/')
def get_brand(request):
    #brand_data =serializers.serialize("json", Brand.objects.all())
    brand_data =Brand.objects.all()
    return render(request,'setData/index.html',{'brand_data':brand_data })
#修改品牌
@login_required(login_url='/login/')
def modify_brand(request):

    brand_data =Brand.objects.all()
    return render(request,'setData/index.html',{'brand_data':brand_data })

    # id = request.get['id']
    # brand_data =BrandType.objects.filter(id=id)
    # return render(request,'setData/test.html',{'modify_brand':modify_brand })


#新加型号
@login_required(login_url='/login/')
def create_brandtype(request):
    if request.method == 'POST':
        form = brandtypeForm(request.POST)
        if form.is_valid():
            #data = form.clean()
            brand=form.cleaned_data['brand']
            brandtype=form.cleaned_data['brandtype']

            val = BrandType.objects.filter(name=brand)
            if not val:
                dtime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                #un_time = time.mktime(dtime.timetuple())
                BrandType.objects.create(
                    name=brandtype,
                    brand_name=brand,
                    create_time=dtime,
                    who_create=request.user.username
                    )
            else:
                dtime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                #un_time = time.mktime(dtime.timetuple())

                BrandType.objects.filter(name=brand).update(
                    name=brandtype,
                    brand_name=brand,
                    create_time=dtime,
                    who_create=request.user.username
                    )
            brandtype_data = BrandType.objects.all()
            return render(request,'setData/brandtype.html',{'brandtype_data':brandtype_data })
        else:
            error = form.errors
            return render(request,'setData/brandtype.html',{'form_error':error})
    else:
        return HttpResponse ('create_brandtype 不支持GET请求')

@login_required(login_url='/login/')
def get_brandtype(request):
    brandtype_data = BrandType.objects.all()
    return render(request,'setData/brandtype.html',{'brandtype_data':brandtype_data })
