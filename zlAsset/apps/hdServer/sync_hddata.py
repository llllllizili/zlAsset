# coding: utf -8
import os
import sys
import json
sys.path.append('../')

from tools.ilo.ilo_api import IloApi
from tools.ipmi.ipmi_api import IpmiApi
class SyncHdInfo(object):

    def __init__(self,username,password,server,**kwargs):
        self.username=username
        self.password=password
        self.server=server
        self.ssl=kwargs.get('ssl','')
        self.ilo=''

    def get_hd_info_ilo(self):
        ilo = IloApi(username=self.username,password=self.password,server=self.server)
        ilo.login()
        _ret = ilo.get_info()

        return _ret

    def get_hd_info_ipmi(self):
        ipmi = IpmiApi(username=self.username,password=self.password,server=self.server)
        _ret = ipmi.get_info()

        return _ret

if __name__ == '__main__':
    ilo_login = SyncHdInfo(username='xxxx',password='xxxx',server='192.168.3.11')
    ilo_info = ilo_login.get_hd_info_ilo()

    print (ilo_info)
