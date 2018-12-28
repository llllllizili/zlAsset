# -*- coding:utf-8 -*-
# Author: zili

from django import forms


class departmentForm(forms.Form):
    name = forms.CharField(error_messages={'required': u'部门不能为空'},)
    description = forms.CharField(error_messages={'required': u'职责/描述不能为空'},)

