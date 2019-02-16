# -*- coding:utf-8 -*-
# Author: zili

from django.db import models

# Create your models here.


class Data(models.Model):
    hostname = models.CharField(max_length=128,null=True, blank=True)
    host_ip = models.CharField(max_length=128,null=True, blank=True)
    description = models.CharField(max_length=128,null=True, blank=True)
    hdserver_id = models.CharField(max_length=128,null=True, blank=True)
    hdserver_name = models.CharField(max_length=128,null=True, blank=True)
    department = models.CharField(max_length=128,null=True, blank=True)
    team = models.CharField(max_length=128,null=True, blank=True)
    use_member = models.CharField(max_length=128,null=True, blank=True)
    start_date = models.CharField(max_length=128,null=True, blank=True)
    end_date = models.CharField(max_length=128,null=True, blank=True)
    run_env = models.CharField(max_length=128,null=True, blank=True)

    def __str__(self):
        return self.name

class Cert(models.Model):
    os_host_ip=models.CharField(max_length=128,null=True, blank=True)
    ip = models.CharField(max_length=128,null=True, blank=True)
    port = models.CharField(max_length=128,null=True, blank=True)
    os_type = models.CharField(max_length=128,null=True, blank=True)
    username = models.CharField(max_length=128,null=True, blank=True)
    password = models.CharField(max_length=128,null=True, blank=True)
    sync = models.CharField(max_length=128,null=True, blank=True)

    def __str__(self):
        return self.ip

class SyncData(models.Model):
    cert_ip=models.CharField(max_length=128,null=True, blank=True)
    host_ip=models.CharField(max_length=128,null=True, blank=True)
    hostname=models.CharField(max_length=128,null=True, blank=True)
    os_sys=models.CharField(max_length=128,null=True, blank=True)
    os_version=models.CharField(max_length=128,null=True, blank=True)
    os_kernel = models.CharField(max_length=128,null=True, blank=True)
    cpu_model = models.TextField(null=True, blank=True)
    cpu_num = models.CharField(max_length=128,null=True, blank=True)
    cpu_core=models.CharField(max_length=128,null=True, blank=True)
    mem_total=models.CharField(max_length=128,null=True, blank=True)
    disk_total=models.CharField(max_length=128,null=True, blank=True)
    product_id=models.CharField(max_length=128,null=True, blank=True)
    phydisk=models.TextField(null=True, blank=True)
    logicdisk=models.TextField(null=True, blank=True)
    install_date=models.CharField(max_length=128,null=True, blank=True)
    network = models.TextField(null=True, blank=True)
    update_time=models.CharField(max_length=128,null=True, blank=True)
    netstat=models.TextField(null=True, blank=True)

    def __str__(self):
        return self.host_ip

#models.TextField(null=True, blank=True)
