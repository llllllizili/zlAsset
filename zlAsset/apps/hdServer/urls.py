# -*- coding:utf-8 -*-
from django.urls import path,include
from . import views

urlpatterns = [
    path('info/',views.get_hd_info,name='get_hd_info'),
    path('task_add_test/',views.task_add_test,name='task_add_test'),
]
