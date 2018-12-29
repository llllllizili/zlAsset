# -*- coding:utf-8 -*-
# Author: zili

from django import forms


class departmentForm(forms.Form):
    name = forms.CharField(error_messages={'required': u'部门不能为空'},)
    description = forms.CharField(error_messages={'required': u'职责/描述不能为空'},)

class teamForm(forms.Form):
    name = forms.CharField(error_messages={'required': u'团队不能为空'},)
    description = forms.CharField(error_messages={'required': u'职责/描述不能为空'},)
    department = forms.CharField(error_messages={'required': u'所属部门不能为空'},)

class memberForm(forms.Form):
    name = forms.CharField(error_messages={'required': u'姓名不能为空'},)
    team = forms.CharField(error_messages={'required': u'团队不能为空'},)
    phone = forms.CharField(error_messages={'required': u'电话不能为空'},)
    email = forms.CharField(error_messages={'required': u'邮箱不能为空'},)
