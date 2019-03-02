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
    path('add_job_action/',views.add_job_action,name='automation_add_job_action'),
    path('test_job/',views.test_job,name='automation_test_job'),
    # path('test_job_save/',views.test_job_save,name='automation_test_job_save'),
    # path('test_job_action/',views.test_job_action,name='automation_test_job_action'),
    path('delete_job/<int:id>/',views.delete_job,name='automation_delete_job'),
    path('modify_job/<int:id>/',views.modify_job,name='automation_modify_job'),
    path('job_detail/<int:id>/',views.job_detail,name='automation_job_detail'),
]+ static(settings.STATIC_URL, document_root = settings.STATIC_ROOT)
