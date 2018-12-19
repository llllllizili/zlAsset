from django import forms


class brandForm(forms.Form):
    name = forms.CharField(error_messages={'required': u'品牌名不能为空'},)
