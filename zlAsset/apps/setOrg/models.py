# -*- coding:utf-8 -*-
# Author: zili

from django.db import models

# Create your models here.


class Department(models.Model):
    name = models.CharField(max_length=128)#unique=True
    description = models.CharField(max_length=128,null=True, blank=True)

    def __str__(self):
        return self.name

class Team(models.Model):
    name = models.CharField(max_length=128)#unique=True
    description = models.CharField(max_length=128,null=True, blank=True)
    # 表关联
    department = models.ForeignKey('Department',null=True, blank=True, on_delete=models.SET_NULL)
    department_name = models.CharField(max_length=128,null=True, blank=True)

    def __str__(self):
        return self.name

class Member(models.Model):
    name = models.CharField(max_length=128)#unique=True
    # 表关联
    team = models.ForeignKey('Team',null=True, blank=True, on_delete=models.SET_NULL)
    team_name = models.CharField(max_length=128,null=True, blank=True)
    email = models.CharField(max_length=128,null=True, blank=True)
    phone = models.CharField(max_length=128,null=True, blank=True)

    def __str__(self):
        return self.name

