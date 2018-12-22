from django.shortcuts import render,HttpResponse
from django.http import JsonResponse
from urllib.parse import quote, unquote

from django.core import serializers

from django.contrib.auth.decorators import login_required
# Create your views here.
import time,datetime
from .models import Brand,BrandType
from .forms import brandForm

@login_required(login_url='/login/')
def index(request):
    # brand_data = Brand.objects.all()
    # return render(request,'setData/index.html',{'brand_data':brand_data })
    return render(request,'setData/index.html')

#新加品牌
@login_required(login_url='/login/')
def create_brand(request):
    if request.method == 'POST':
        form = brandForm(request.POST)
        if form.is_valid():
            data = form.clean()
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
            return render(request,'setData/index.html')
        else:
            error = form.errors
            return render(request,'setData/index.html')
    else:
        return HttpResponse ('不支持GET请求')

#查找品牌
@login_required(login_url='/login/')
def get_brand(request):
    brand_data =serializers.serialize("json", Brand.objects.all())
    return render(request,'setData/index.html',{'brand_data':brand_data })

#查找品牌类型
@login_required(login_url='/login/')
def get_brandtype(request):
    brandtype_data =serializers.serialize("json", BrandType.objects.all())
    return JsonResponse({'brandtype_data':brandtype_data })

