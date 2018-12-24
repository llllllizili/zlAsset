from django import forms


class brandForm(forms.Form):
    name = forms.CharField(error_messages={'required': u'品牌名不能为空'},)

class brandtypeForm(forms.Form):
    brand = forms.CharField(error_messages={'required': u'品牌名不能为空'},)
    brandtype = forms.CharField(error_messages={'required': u'型号不能为空'},)

class positionForm(forms.Form):
    name = forms.CharField(error_messages={'required': u'名称不能为空'},)
    city = forms.CharField(error_messages={'required': u'城市不能为空'},)
    address = forms.CharField(error_messages={'required': u'地址不能为空'},)
