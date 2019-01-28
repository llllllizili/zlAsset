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

class OsData(viewsets.ViewSet):
    def list(self,request):
        queryset = Data.objects.all()
        serializer_class = DataSerializer
        serializer = DataSerializer(queryset, many=True)
        if serializer.data == []:
            return Response('None')
        else:
            return Response(serializer.data)