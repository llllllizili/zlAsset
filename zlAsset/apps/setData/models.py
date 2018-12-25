# -*- coding:utf-8 -*-
# Author: zili

from django.db import models

# Create your models here.


class Brand(models.Model):
    name = models.CharField(max_length=128)#unique=True
    create_time = models.CharField(max_length=128,null=True, blank=True)
    who_create = models.CharField(max_length=128,null=True, blank=True)

    def __str__(self):
        return self.name

class BrandType(models.Model):
    name = models.CharField(max_length=128)#unique=True
    # 表关联
    brand = models.ForeignKey('Brand',null=True, blank=True, on_delete=models.SET_NULL)
    brand_name = models.CharField(max_length=128,null=True, blank=True)
    create_time = models.CharField(max_length=128,null=True, blank=True)
    who_create = models.CharField(max_length=128,null=True, blank=True)

    def __str__(self):
        return self.name

class Position(models.Model):
    name = models.CharField(max_length=128)#unique=True
    # 表关联
    city = models.CharField(max_length=128,null=True, blank=True)
    address = models.CharField(max_length=128,null=True, blank=True)

    def __str__(self):
        return self.name

class DataCenter(models.Model):
    name = models.CharField(max_length=128)#unique=True
    # 表关联
    position = models.ForeignKey('Position',null=True, blank=True, on_delete=models.SET_NULL)
    position_name = models.CharField(max_length=128,null=True, blank=True)
    city = models.CharField(max_length=128,null=True, blank=True)
    address = models.CharField(max_length=128,null=True, blank=True)
    type = models.CharField(max_length=128,null=True, blank=True)
    supplier = models.CharField(max_length=128,null=True, blank=True)
    supplier_phone = models.CharField(max_length=128,null=True, blank=True)
    manager = models.CharField(max_length=128,null=True, blank=True)
    manager_phone = models.CharField(max_length=128,null=True, blank=True)

    def __str__(self):
        return self.name

