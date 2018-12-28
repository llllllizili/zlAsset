# -*- coding:utf-8 -*-
# Author: zili

# -*- coding:utf-8 -*-
# Author: zili

from django.urls import path,include
from django.conf.urls import url
#静态文件
from django.conf.urls.static import static
from django.conf import settings
from . import views
# from . import api as api_views

# from rest_framework.routers import DefaultRouter
# router = DefaultRouter()

#api

# /setOrg/api/get_department/  # userd: setOrg/departmenttype.html
# router.register('get_department',api_views.departmentData,base_name='setOrg_get_department_api')


urlpatterns = [
    path('',views.index,name='setOrg_index'),#index:member

    path('create_department/',views.create_department,name='setOrg_create_department'),
    path('get_department/',views.get_department,name='setOrg_get_department'),
    path('delete_department/<int:id>/',views.delete_department,name='setOrg_delete_department'),
    path('modify_department/<int:id>/',views.modify_department,name='setOrg_modify_department'),
    path('modify_department_action/',views.modify_department_action,name='setOrg_modify_department_action'),


    #api
    # url(r'^api/', include(router.urls)),
]+ static(settings.STATIC_URL, document_root = settings.STATIC_ROOT)
