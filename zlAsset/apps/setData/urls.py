# -*- coding:utf-8 -*-
# Author: zili

from django.urls import path,include
#静态文件
from django.conf.urls.static import static
from django.conf import settings
from . import views

urlpatterns = [
    path('',views.index,name='setData_index'),
    path('create_brand_action/',views.create_brand_action,name='setData_create_brand_action'),
]+ static(settings.STATIC_URL, document_root = settings.STATIC_ROOT)
