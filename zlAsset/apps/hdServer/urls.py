# -*- coding:utf-8 -*-
from django.urls import path,include
#静态文件
from django.conf.urls.static import static
from django.conf import settings
from . import views

urlpatterns = [
    path('index/',views.index,name='hdServer_index'),
    path('add_hd/',views.add_hd,name='hdServer_add_hd'),
    path('add_hd_action/',views.add_hd_action,name='hdServer_add_hd_action'),
    path('modify_hd/<int:id>/',views.modify_hd,name='hdServer_modify_hd'),
    path('modify_hd_action/',views.modify_hd_action,name='hdServer_modify_hd_action'),
    path('base_detail/<int:id>/',views.base_detail,name='hdServer_base_detail'),

    path('test/',views.test,name='hdServer_test'),
    path('info/',views.get_hd_info,name='hdServer_get_info'),
    path('task_add_test/',views.task_add_test,name='task_add_test'),
]+ static(settings.STATIC_URL, document_root = settings.STATIC_ROOT)
