# -*- coding:utf-8 -*-
# Author: zili

from django.urls import path,include
from django.conf.urls import url
#静态文件
from django.conf.urls.static import static
from django.conf import settings
from . import views
from . import api as api_views

from rest_framework.routers import DefaultRouter
router = DefaultRouter()

#api


# /setData/api/get_brandtype/  # userd: setData/brandtype.html
router.register('get_brand',api_views.BrandData,base_name='setData_get_brand_api')
# /setData/api/get_brandtype/  # userd: setData/index.html
router.register('get_brandtype',api_views.BrandTypeData,base_name='setData_get_brandtype_api')

urlpatterns = [
    path('',views.index,name='setData_index'),
    path('create_brand/',views.create_brand,name='setData_create_brand'),
    path('get_brand/',views.get_brand,name='setData_get_brand'),
    path('modify_brand/',views.modify_brand,name='setData_modify_brand'),

    path('create_brandtype/',views.create_brandtype,name='setData_create_brandtype'),
    path('get_brandtype/',views.get_brandtype,name='setData_get_brandtype'),


    #api
    url(r'^api/', include(router.urls)),
]+ static(settings.STATIC_URL, document_root = settings.STATIC_ROOT)
