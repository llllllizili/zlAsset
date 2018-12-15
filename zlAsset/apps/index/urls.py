# -*- coding:utf-8 -*-
from django.urls import path,include
#静态文件
from django.conf.urls.static import static
from django.conf import settings
from . import views

urlpatterns = [
    path('',views.index,name='index_index'),
    path('index/',views.index,name='index_index'),
    path('login/',views.login,name='index_login'),
]+ static(settings.STATIC_URL, document_root = settings.STATIC_ROOT)
