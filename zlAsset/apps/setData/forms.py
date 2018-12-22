from django import forms


class brandForm(forms.Form):
    name = forms.CharField(error_messages={'required': u'品牌名不能为空'},)

class brandtypeForm(forms.Form):
    brand = forms.CharField(error_messages={'required': u'品牌名不能为空'},)
    brandtype = forms.CharField(error_messages={'required': u'型号不能为空'},)
