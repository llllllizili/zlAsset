# -*- coding:utf-8 -*-
from django.urls import path,include
from django.conf.urls import url
#静态文件
from django.conf.urls.static import static
from django.conf import settings
from . import views

# from rest_framework.routers import DefaultRouter
# router = DefaultRouter()


urlpatterns = [
    path('index/',views.index,name='atuomation_index'),
    path('add_job/',views.add_job,name='automation_add_job'),
]+ static(settings.STATIC_URL, document_root = settings.STATIC_ROOT)
