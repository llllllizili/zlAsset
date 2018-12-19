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

# class HostHDIlo(models.Model):
#     host_ip = models.CharField(max_length=128)#unique=True
#     way = models.CharField(max_length=128,null=True, blank=True)
#     net_num = models.CharField(max_length=128,null=True, blank=True)
#     net_mac = models.TextField(max_length=128,null=True, blank=True)
#     mem = models.TextField(null=True, blank=True)
#     uuid = models.CharField(max_length=128,null=True, blank=True)
#     cpu_info = models.TextField(null=True, blank=True)
#     disk_info = models.TextField(null=True, blank=True)
#     raid_info = models.TextField(null=True, blank=True)
#     power_type = models.CharField(max_length=128,null=True, blank=True)
#     #fan_speed = models.CharField(max_length=128,null=True, blank=True)
#     fw_ver = models.CharField(max_length=128,null=True, blank=True)
#     #power_watt = models.CharField(max_length=128,null=True, blank=True)
#     sn = models.CharField(max_length=128,null=True, blank=True)
#     product_name = models.CharField(max_length=128,null=True, blank=True)
#     ilo_log = models.TextField(null=True, blank=True)
#     license = models.CharField(max_length=128,null=True, blank=True)

#     def __unicode__(self):
#         return self.host_ip
