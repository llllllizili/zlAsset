# coding: utf-8

import os
from .ansible_api import MyApi as AnsibleApi
# from ansible_api import MyApi as AnsibleApi #if __name__使用

import logging
logger = logging.getLogger(__name__)


class RemoteRun(object):
    global script_path
    script_path = os.path.dirname(__file__) + '/script/'
    def __init__(self,**kwargs):
        self.ip=kwargs.get('ip','')
        self.username=kwargs.get('username','')
        self.password=kwargs.get('password','')
        self.port=kwargs.get('port',22)
        self.os_type=kwargs.get('os_type')
        self.time_out = kwargs.get('time_out',10)
        self.run_user = kwargs.get('become_user','root')

        if not self.os_type :
            return 'OS TYPE 未配置'
        if not self.ip:
            return 'ip 未配置'
        if self.os_type.lower() == 'linux':
            if not self.username or not self.password:
                return '账号,密码不完整'

        self.sources=[]
        host_info={}

        host_info['hostname']=self.ip
        host_info['ansible_user']=self.username
        host_info['ansible_ssh_pass']=self.password
        host_info['ansible_port']=self.port

        self.sources.append(host_info)




    def get_path(self):
        return script_path

    def run_cmd(self,cmd,**kwargs):
        chdir=kwargs.get('chdir','')
        if cmd:
            if len(self.sources)>0:
                ansible_run = AnsibleApi(resource=self.sources)
                ansible_run.run(self.ip, 'shell', 'source /etc/profile;'+cmd +
                    ' chdir='+chdir if chdir else cmd )
                data=ansible_run.get_result()

                success_data=data['success']
                failed_data=data['failed']
                unreachable_data=data['unreachable']

                return_data=dict()


                if len(failed_data) > 0:
                    return_data['status']='failed'
                    return_data['result']=failed_data[self.ip]['command']
                    return return_data
                if len(unreachable_data) >0:
                    return_data['status']='unreachable'
                    return_data['result']=unreachable_data[self.ip]['command']
                    return return_data
                else:
                    return_data['status']='success'
                    return_data['result']=success_data[self.ip]['command']
                    return return_data
        else:
            pass

    def run_script(self,script,options):
        if len(self.sources)>0:
            ansible_run = AnsibleApi(
                    resource=self.sources,
                    become_user=self.run_user,
                    timeout=self.time_out,
                )
            logger.info(str(script_path+script))
            print(script_path+script)
            ansible_run.run(self.ip, 'script', script_path+script + ' ' + options)
            data=ansible_run.get_result()

            success_data=data['success']
            failed_data=data['failed']
            unreachable_data=data['unreachable']

            return_data=dict()

            if len(failed_data) > 0:
                return_data['status']='failed'
                return_data['result']=failed_data[self.ip]['script']
                logger.error(self.ip + str(return_data))
                return return_data
            if len(unreachable_data) >0:

                return_data['status']='unreachable'
                return_data['result']=unreachable_data[self.ip]['script']
                logger.error(self.ip + str(return_data))
                return return_data
            else:
                return_data['status']='success'
                return_data['result']=success_data[self.ip]['script']
                logger.info(self.ip + str(return_data))
                return return_data
        else:
            pass

    def run_copy(self):
        pass

def get_script_path():
    path = os.path.dirname(__file__) + '/script/'
    return path
if __name__ == '__main__':
    # from ansible_api import MyApi as AnsibleApi #if __name__使用 开头替换
    run = RemoteRun(ip='192.168.1.55',username='test',password='centos',port=22,os_type='linux')
    d = run.run_cmd('rm -rf /123')
    print(d)
    # dd = run.run_cmd('ls /opt123')
    # print(dd)

    # rund = RemoteRun(ip='192.168.1.1131',username='root',password='centos',port=22,os_type='linux')
    # ddd = rund.run_cmd('ls /opt123')
    # print(ddd)
