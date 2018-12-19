from django.shortcuts import render,HttpResponse
from urllib.parse import quote, unquote

from django.contrib.auth.decorators import login_required
# Create your views here.
import time,datetime
from .models import Brand,BrandType
from .forms import brandForm

@login_required(login_url='/login/')
def index(request):
    return render(request, 'setData/index.html')

@login_required(login_url='/login/')
def create_brand(request):
    return render(request, 'setData/brand.html')

@login_required(login_url='/login/')
def create_brand_action(request):
    if request.method == 'POST':
        form = brandForm(request.POST)
        if form.is_valid():
            data = form.clean()
            name=form.cleaned_data['name']
            val = Brand.objects.filter(name=name)
            if not val:
                dtime = datetime.datetime.now()
                un_time = time.mktime(dtime.timetuple())

                Brand.objects.create(
                    name=name,
                    create_time=un_time,
                    who_create=request.user.username
                    )
            else:
                dtime = datetime.datetime.now()
                un_time = time.mktime(dtime.timetuple())

                Brand.objects.filter(name=name).update(
                    name=name,
                    create_time=un_time,
                    who_create=request.user.username
                    )
            return render(request,'setData/brand.html')
        else:
            error = form.errors
            return render(request,'setData/brand.html')
    else:
        return HttpResponse ('不支持GET请求')


