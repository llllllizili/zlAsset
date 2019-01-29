# -*- coding:utf-8 -*-
from django.urls import path,include
#静态文件
from django.conf.urls.static import static
from django.conf import settings
from . import views




urlpatterns = [
    path('index/',views.index,name='operSystem_index'),
    path('add_os/',views.add_os,name='operSystem_add_os'),
    path('add_os_action/',views.add_os_action,name='operSystem_add_os_action'),
    path('delete_os/<int:id>/',views.delete_os,name='operSystem_delete_os'),
    path('modify_os/<int:id>/',views.modify_os,name='operSystem_modify_os'),
    path('modify_os_action/',views.modify_os_action,name='operSystem_modify_os_action'),
    path('base_detail/<int:id>/',views.base_detail,name='operSystem_base_detail'),
    path('sync_detail/<int:id>/',views.sync_detail,name='operSystem_sync_detail'),
    path('set_cert/<int:id>/',views.set_cert,name='operSystem_set_cert'),
    path('set_sync/<int:id>/',views.set_sync,name='operSystem_set_sync'),

    path('test/',views.test,name='operSystem_test'),
    #path('task_add_test/',views.task_add_test,name='task_add_test'),
]+ static(settings.STATIC_URL, document_root = settings.STATIC_ROOT)
