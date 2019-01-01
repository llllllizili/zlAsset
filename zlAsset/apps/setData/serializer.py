# -*- coding:utf-8 -*-
# Author: zili

from rest_framework import serializers
from .models import *

class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model =Brand
        fields =('id','name','create_time','who_create')

class BrandTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model =BrandType
        fields =('id','name','brand_id','brand_name','create_time','who_create')
class PositionSerializer(serializers.ModelSerializer):
    class Meta:
        model =Position
        fields =('id','name','city','address')
class DatacenterSerializer(serializers.ModelSerializer):
    class Meta:
        model =DataCenter
        fields =('id','name','position_id','position_name')
