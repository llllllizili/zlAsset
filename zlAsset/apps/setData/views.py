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
        return HttpResponseRedirect ('/setData/index/')
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
        return HttpResponseRedirect ('/setData/index/')
#删除品牌
@login_required(login_url='/login/')
def delete_brand(request,id):
    #id = request.GET['id']
    #id = request.GET.get('id', '')
    val = BrandType.objects.filter(brand_id=id)
    if val:
        error_data='请先删除相关型号'
        brand_data =Brand.objects.all()
        return render(request,'setData/index.html',{'brand_data':brand_data,'error_data':error_data })
    else:
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
            brand_info =Brand.objects.get(name=brand)
            if not val:
                dtime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                #un_time = time.mktime(dtime.timetuple())
                BrandType.objects.create(
                    name=brandtype,
                    brand_name=brand,
                    create_time=dtime,
                    who_create=request.user.username,
                    brand_id=brand_info.id
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
        return HttpResponseRedirect ('/setData/get_brandtype/')
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
        brand_info =Brand.objects.get(name=brand)
        BrandType.objects.filter(id=id).update(
                    name=brandtype,
                    brand_name=brand,
                    create_time=dtime,
                    who_create=request.user.username,
                    brand_id=brand_info.id
                    )
        brandtype_data =BrandType.objects.all()
        return render(request,'setData/brandtype.html',{'brandtype_data':brandtype_data })
    else:
        return HttpResponseRedirect ('/setData/get_brandtype/')

#删除型号
@login_required(login_url='/login/')
def delete_brandtype(request,id):
    BrandType.objects.filter(id=id).delete()
    brandtype_data =BrandType.objects.all()
    return render(request,'setData/brandtype.html',{'brandtype_data':brandtype_data })


#添加地理位置
@login_required(login_url='/login/')
def create_position(request):
    if request.method == 'POST':
        form = positionForm(request.POST)
        if form.is_valid():
            #data = form.clean()
            name=form.cleaned_data['name']
            city=form.cleaned_data['city']
            address=form.cleaned_data['address']

            val = Position.objects.filter(name=name)
            if not val:
                Position.objects.create(
                    name=name,
                    city=city,
                    address=address,
                    )
                position_data = Position.objects.all()
                return render(request,'setData/position.html',{'position_data':position_data })

            else:
                error_data = city + ' 已存在'
                position_data = Position.objects.all()
                return render(request,'setData/position.html',{'position_data':position_data,'error_data':error_data})
        else:
            error = form.errors
            return render(request,'setData/position.html',{'form_error':error})
    else:
        return HttpResponseRedirect ('/setData/get_position/')
#获取地理位置
@login_required(login_url='/login/')
def get_position(request):
    position_data = Position.objects.all()
    return render(request,'setData/position.html',{'position_data':position_data })
#修改地理位置
def modify_position(request,id):
    position_data =Position.objects.get(id=id)
    return render(request,'setData/modify_position.html',{'position_data':position_data })
@login_required(login_url='/login/')
def modify_position_action(request):
    if request.method == 'POST':
        id=int(request.POST['id'])
        name=request.POST['name']
        city=request.POST['city']
        address=request.POST['address']

        Position.objects.filter(id=id).update(
                    name=name,
                    city=city,
                    address=address,
                    )
        position_data =Position.objects.all()
        return render(request,'setData/position.html',{'position_data':position_data })
    else:
        return HttpResponseRedirect ('/setData/get_position/')
#删除地理位置
@login_required(login_url='/login/')
def delete_position(request,id):
    val = DataCenter.objects.filter(position_id=id)
    if val:
        error_data='请先删除相关数据中心'
        position_data =Position.objects.all()
        return render(request,'setData/position.html',{'position_data':position_data,'error_data':error_data })
    else:
        Position.objects.filter(id=id).delete()
        position_data =Position.objects.all()
        return render(request,'setData/position.html',{'position_data':position_data })
#添加数据中心
@login_required(login_url='/login/')
def create_datacenter(request):
    if request.method == 'POST':
        form = datacenterForm(request.POST)
        if form.is_valid():
            #data = form.clean()
            name=form.cleaned_data['name']
            position_name=form.cleaned_data['position_name']
            type=form.cleaned_data['type']
            supplier=form.cleaned_data['supplier']
            supplier_phone=form.cleaned_data['supplier_phone']
            manager=form.cleaned_data['manager']
            manager_phone=form.cleaned_data['manager_phone']

            val = DataCenter.objects.filter(name=name)
            position_info = Position.objects.get(name=position_name)
            if not val:
                DataCenter.objects.create(
                    name=name,
                    position_name=position_name,
                    type=type,
                    supplier=supplier,
                    supplier_phone=supplier_phone,
                    manager=manager,
                    manager_phone=manager_phone,
                    position_id=position_info.id,
                    city=position_info.city,
                    address=position_info.address
                    )
                datacenter_data = DataCenter.objects.all()
                return render(request,'setData/datacenter.html',{'datacenter_data':datacenter_data })

            else:
                error_data = name + ' 已存在'
                datacenter_data = DataCenter.objects.all()
                return render(request,'setData/datacenter.html',{'datacenter_data':datacenter_data,'error_data':error_data})
        else:
            error = form.errors
            return render(request,'setData/datacenter.html',{'form_error':error})
    else:
        return HttpResponseRedirect ('/setData/get_datacenter/')
#获取数据中心
@login_required(login_url='/login/')
def get_datacenter(request):
    datacenter_data = DataCenter.objects.all()
    return render(request,'setData/datacenter.html',{'datacenter_data':datacenter_data })
#修改数据中心
def modify_datacenter(request,id):
    datacenter_data =DataCenter.objects.get(id=id)
    return render(request,'setData/modify_datacenter.html',{'datacenter_data':datacenter_data })
@login_required(login_url='/login/')
def modify_datacenter_action(request):
    if request.method == 'POST':
        id=int(request.POST['id'])
        name=request.POST['name']
        position_name=request.POST['position_name']
        type=request.POST['type']
        supplier=request.POST['supplier']
        supplier_phone=request.POST['supplier_phone']
        manager=request.POST['manager']
        manager_phone=request.POST['manager_phone']

        position_info = Position.objects.get(name=position_name)
        DataCenter.objects.filter(id=id).update(
                    name=name,
                    position_name=position_name,
                    type=type,
                    supplier=supplier,
                    supplier_phone=supplier_phone,
                    manager=manager,
                    manager_phone=manager_phone,
                    position_id=position_info.id,
                    city=position_info.city,
                    address=position_info.address
                    )
        datacenter_data =DataCenter.objects.all()
        return render(request,'setData/datacenter.html',{'datacenter_data':datacenter_data })
    else:
        return HttpResponseRedirect ('/setData/get_datacenter/')
#删除数据中心
@login_required(login_url='/login/')
def delete_datacenter(request,id):
    DataCenter.objects.filter(id=id).delete()
    datacenter_data =DataCenter.objects.all()
    return render(request,'setData/datacenter.html',{'datacenter_data':datacenter_data })
