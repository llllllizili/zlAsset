# -*- coding:utf-8 -*-
# Author: zili

from rest_framework import serializers
from .models import *

class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model =Department
        fields =('id','name','description')

class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model =Team
        fields =('id','name','description')
