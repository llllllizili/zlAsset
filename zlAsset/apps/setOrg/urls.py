# -*- coding:utf-8 -*-
# Author: zili

# -*- coding:utf-8 -*-
# Author: zili

from django.urls import path,include
from django.conf.urls import url
#静态文件
from django.conf.urls.static import static
from django.conf import settings
from .import views
from .import api as api_views

from rest_framework.routers import DefaultRouter
router = DefaultRouter()

#api

# /setOrg/api/get_department/  # userd: setOrg/team.html
router.register('get_department',api_views.DepartmentData,base_name='setOrg_get_department_api')
router.register('get_team',api_views.TeamData,base_name='setOrg_get_team_api')


urlpatterns = [
    path('',views.index,name='setOrg_index'),#index:member

    path('create_department/',views.create_department,name='setOrg_create_department'),
    path('get_department/',views.get_department,name='setOrg_get_department'),
    path('delete_department/<int:id>/',views.delete_department,name='setOrg_delete_department'),
    path('modify_department/<int:id>/',views.modify_department,name='setOrg_modify_department'),
    path('modify_department_action/',views.modify_department_action,name='setOrg_modify_department_action'),

    path('create_team/',views.create_team,name='setOrg_create_team'),
    path('get_team/',views.get_team,name='setOrg_get_team'),
    path('delete_team/<int:id>/',views.delete_team,name='setOrg_delete_team'),
    path('modify_team/<int:id>/',views.modify_team,name='setOrg_modify_team'),
    path('modify_team_action/',views.modify_team_action,name='setOrg_modify_team_action'),

    path('create_member/',views.create_member,name='setOrg_create_member'),
    path('get_member/',views.get_member,name='setOrg_get_member'),
    path('delete_member/<int:id>/',views.delete_member,name='setOrg_delete_member'),
    path('modify_member/<int:id>/',views.modify_member,name='setOrg_modify_member'),
    path('modify_member_action/',views.modify_member_action,name='setOrg_modify_member_action'),

    #api
    url(r'^api/', include(router.urls)),
]+ static(settings.STATIC_URL, document_root = settings.STATIC_ROOT)
