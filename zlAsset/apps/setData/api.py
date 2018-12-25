# -*- coding:utf-8 -*-
# Author: zili

# data db
from .models import *

#rest framework
import django_filters
from rest_framework import viewsets, filters
#from rest_framework.decorators import api_view
#from rest_framework import mixins
#from rest_framework import generics
#from rest_framework.views import APIView
#from rest_framework import status
from rest_framework.response import Response

#serializer
from .serializer import *

class BrandData(viewsets.ViewSet):
    def list(self,request):
        queryset = Brand.objects.all()
        serializer_class = BrandSerializer
        serializer = BrandSerializer(queryset, many=True)
        if serializer.data == []:
            return Response('None')
        else:
            return Response(serializer.data)

class BrandTypeData(viewsets.ViewSet):
    def list(self,request):
        queryset = BrandType.objects.all()
        serializer_class = BrandTypeSerializer
        serializer = BrandTypeSerializer(queryset, many=True)
        if serializer.data == []:
            return Response('None')
        else:
            return Response(serializer.data)

class PositionData(viewsets.ViewSet):
    def list(self,request):
        queryset = Position.objects.all()
        serializer_class = PositionSerializer
        serializer = PositionSerializer(queryset, many=True)
        if serializer.data == []:
            return Response('None')
        else:
            return Response(serializer.data)
