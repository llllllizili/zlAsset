# -*- coding:utf-8 -*-
# Author: zili

from rest_framework import serializers
from .models import *

class DataSerializer(serializers.ModelSerializer):
    class Meta:
        model =Data
        fields =('id','name')
