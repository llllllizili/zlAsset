# -*- coding:utf-8 -*-
# Author: zili

from django.db import models

# Create your models here.


class Jobs(models.Model):
    name = models.CharField(max_length=128,null=True, blank=True)
    description = models.CharField(max_length=128,null=True, blank=True)
    script_name = models.CharField(max_length=32,null=True, blank=True)
    create_time = models.CharField(max_length=128,null=True, blank=True)
    user = models.CharField(max_length=32,null=True, blank=True)

    def __str__(self):
        return self.name
