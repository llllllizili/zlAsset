# -*- coding:utf-8 -*-
# Author: zili
import os
import sys
import json
sys.path.append('../')
from tools.ansible.run_api import RemoteRun as RunAnsibleApi
from tools.ansible.run_api import get_script_path


class RunAutomation(object):
    def __init__(self,**kwargs):
        self.ip=kwargs.get('ip','')
        self.username=kwargs.get('username','')
        self.password=kwargs.get('password','')
        self.port=kwargs.get('port',22)
        self.os_type=kwargs.get('os_type')

        self.ansible_run = RunAnsibleApi(
                ip=self.ip,
                username=self.username,
                password=self.password,
                port=self.port,
                os_type=self.os_type
            )

    def command(self,cmd):
        cmd = cmd
        data = self.ansible_run.run_cmd(cmd)
        return data
    # def script_test(self):
    #     data = self.ansible_run.run_script('operSystem/test.sh','')
    #     return data

    # def get_os_info(self):
    #     data = self.ansible_run.run_script('operSystem/os_base_info.sh','')
    #     return data

def script_path():
    p = get_script_path()
    return p
if __name__ == '__main__':
    l = RunAutomation(ip='192.168.1.55',username='test',password='centos',port='22',os_type='linux')
    cmd="ip addr"
    data = l.command(str(cmd))
    print(data)
