# -*- coding:utf-8 -*-
from __future__ import absolute_import
from celery import shared_task
from celery.task import task

from models import *
import time


@task
def add(x, y):
    time.sleep(10)
    return int(x) + int(y)

@task
def print_hello():
    return 'hello celery and django...'
# @shared_task
# def zili(x, y):
#     time.sleep(10)
#     return int(x) + int(y)

# #hdServer sync ipmi info
# @shared_task
# def ipmi_sync():
#     cert_data=Cert.objects.all()
#     for c in cert_data:
#         if c.sync=='true':
#             if c.way=='ipmi':
#                 ipmi_login = SyncHdInfo(username=c.username,password=c.password,server=c.ip)
#                 ipmi_info = ipmi_login.get_hd_info_ipmi()

#                 update_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
#                 val = IpmiData.objects.filter(cert_ip=c.ip)
#                 if not val:
#                     IpmiData.objects.create(
#                         cert_ip=c.ip,
#                         brand=ipmi_info['hd']['brand'],
#                         product_name=ipmi_info['hd']['product_name'],
#                         uuid=ipmi_info['uuid'],
#                         fw=ipmi_info['fw'],
#                         way='ipmi',
#                         ip=ipmi_info['net']['IPAddress'],
#                         mac=ipmi_info['net']['MACAddress'],
#                         sn=ipmi_info['hd']['sn'],
#                         update_time=update_time
#                     )
#                     return 'sync success'
#                 else:
#                     IpmiData.objects.filter(cert_ip=c.ip).update(
#                         cert_ip=c.ip,
#                         brand=ipmi_info['hd']['brand'],
#                         product_name=ipmi_info['hd']['product_name'],
#                         uuid=ipmi_info['uuid'],
#                         fw=ipmi_info['fw'],
#                         way='ipmi',
#                         ip=ipmi_info['net']['IPAddress'],
#                         mac=ipmi_info['net']['MACAddress'],
#                         sn=ipmi_info['hd']['sn'],
#                         update_time=update_time
#                     )
#                     return 'sync update success'
#         return 'disbled sync'
