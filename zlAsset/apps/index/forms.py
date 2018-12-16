# -*- coding:utf-8 -*-


from django import forms


class loginForm(forms.Form):
    username = forms.CharField(error_messages={'required': u'用户名不能为空'},)
    password = forms.CharField(error_messages={'required': u'密码不能为空'},)
