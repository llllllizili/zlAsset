# coding: utf-8
# import commands
import subprocess
import re
import sys
import json
#sys.path.append('../')


IPMI_CMD='ipmitool'

class ServerError(Exception):
    pass

class IpmiApi(object):
    '''
    ipmi api
    '''
    def __init__(self,server,username,password,port=623,interface_type='lanplus'):
        self.server=server
        self.username=username
        self.password=password
        self.port = port
        self.interface=interface_type

    def get_data(self,command):
        (status,output) = subprocess.getstatusoutput(IPMI_CMD + ' -H '+self.server+' -U '+self.username+'\
                         -P '+'"'+self.password+'"'+ ' -p ' + str(self.port) + ' -I ' + self.interface + ' ' +command)

        if status >0:
            return {'status':0,'msg':output}
        else:
            return {'status':1,'msg':output}

    def get_fru(self):
        ret = self.get_data('fru')
        data={}
        start = 0
        for val in ret['msg'].splitlines():
            _v=val.split(':')
            if len(_v) != 2:
                continue
            k=_v[0].strip()
            v=_v[1].strip()

            if k == 'FRU Device Description' and v == 'Builtin FRU Device (ID 0)':
                start =1
            elif k == 'FRU Device Description' and v != 'Builtin FRU Device (ID 0)':
                start = 2
            if start == 1:
                if k == 'Product Name':
                    product_name=v
                    data['product_name']=product_name
                elif k == 'Product Serial':
                    sn=v
                    if sn != '00001':
                        data['sn']=sn
                elif k == 'Board Extra':
                    #if re.match('[a-zA-Z]',v):
                        pass
                elif k == 'Product Manufacturer':
                    brand=v
                    data['brand']=brand
            else:
                continue
        return data


# info
    def get_info(self):
        #fru
        hd = self.get_fru()
        if 'brand' in hd:
            brand=hd['brand']
            #dell
            if 'dell' in brand.lower():
            # uuid info
                uuid_data=''
                uuid = self.get_data('mc guid | grep -i GUID')
                if uuid['status'] == 1:
                    if uuid['msg']:
                        for val in uuid['msg'].splitlines():
                            _v=val.split(':')
                            if len(_v) != 2:
                                continue
                            uuid_data=_v[1].strip()
                        if not uuid_data:
                            uuid_data='unsupported'
                    else:
                        uuid_data='unsupported'
                else:
                    uuid_data='failed (command get uuid)'

                # fw info
                fw_data=''
                fw = self.get_data("mc info | grep -i 'Firmware Revision'")
                if fw['status'] == 1:
                    if fw['msg']:
                        for val in fw['msg'].splitlines():
                            _v=val.split(':')
                            if len(_v) != 2:
                                continue
                            fw_data=_v[1].strip()
                        if not fw_data:
                            fw_data='unsupported'
                    else:
                        fw_data='unsupported'
                else:
                    fw_data='failed (command get fw)'

                # fan info
                fan_num=''
                fan = self.get_data("sensor list | grep -E -i 'fan'")
                if fw['status'] == 1:
                    if fan['msg']:
                        fanlist=[]
                        for val in fan['msg'].splitlines():
                            _v = val.split('|')
                            # hp
                            if 'percent' in _v[2].strip():
                                fanlist.append(_v[0])
                            # lenvov & ibm & dell
                            elif 'RPM' in _v[2].strip():
                                fanlist.append(_v[0])
                            else:
                                continue
                        fan_num = len(fanlist)
                        if not fan_num:
                            fan_num='unsupported'
                    else:
                        fan_num='unsupported'
                else:
                    fan_num='failed (command get fan)'

                #cpu info
                cpu_num=''
                cpu = self.get_data("sensor list | grep -E -i 'CPU'")
                if cpu['status'] == 1:
                    if cpu['msg']:
                        cpulist=[]
                        for val in cpu['msg'].splitlines():
                            _v =  val.split('|')
                            if 'degrees' in _v[2].strip():
                                cpulist.append(_v[0])
                            else:
                                continue
                        cpu_num = len(cpulist)
                        if not cpu_num:
                            cpu_num = 'unsupported'
                    else:
                        cpu_num='unsupported'
                else:
                    cpu_num='failed (command get fan)'

                # mem info
                mem_num=''
                mem = self.get_data("sensor list | grep -E -i 'DIMM'")
                if mem['status'] == 1:
                    if mem['msg']:
                        memlist=[]
                        for val in mem['msg'].splitlines():
                            _v = val.split('|')
                            if 'degrees' in _v[2].strip():
                                memlist.append(_v[0])
                            else:
                                continue
                        mem_num= len(memlist)
                        if not mem_num:
                            mem_num='unsupported'
                    else:
                        mem_num='unsupported'
                else:
                    mem_num='failed (command get mem)'

                # net info
                net_json=''
                net = self.get_data("lan print | grep -E -i 'address|mask'")
                if net['status'] == 1:
                    if net['msg']:
                        net_dict = {}
                        for val in net['msg'].splitlines():
                            _v = val.split(': ')
                            _k = _v[0].strip()
                            net_dict[''.join(_k.split())] = _v[1].strip()
                        if not net_dict:
                            net_json='unsupported'
                        else:
                            net_json=json.dumps(net_dict)
                    else:
                        net_json='unsupported'
                else:
                    net_json='failed (command get net)'

                return {'uuid':uuid_data,'fw':fw_data,'fan_num':fan_num,
                        'cpu_num':cpu_num,'mem_num':mem_num,'net':net_json,
                        'hd':hd}

# other
            else:
            # uuid info
                uuid_data=''
                uuid = self.get_data('mc guid | grep -i GUID')
                if uuid['status'] == 1:
                    if uuid['msg']:
                        for val in uuid['msg'].splitlines():
                            _v=val.split(':')
                            if len(_v) != 2:
                                continue
                            uuid_data=_v[1].strip()
                        if not uuid_data:
                            uuid_data='unsupported'
                    else:
                        uuid_data='unsupported'
                else:
                    uuid_data='failed (command get uuid)'

                # fw info
                fw_data=''
                fw = self.get_data("mc info | grep -i 'Firmware Revision'")
                if fw['status'] == 1:
                    if fw['msg']:
                        for val in fw['msg'].splitlines():
                            _v=val.split(':')
                            if len(_v) != 2:
                                continue
                            fw_data=_v[1].strip()
                        if not fw_data:
                            fw_data='unsupported'
                    else:
                        fw_data='unsupported'
                else:
                    fw_data='failed (command get fw)'


                # fan info
                fan_num=''
                fan = self.get_data("sensor list | grep -E -i 'fan'")
                if fan['status'] == 1:
                    if fan['msg']:
                        fanlist=[]
                        for val in fan['msg'].splitlines():
                            if 'fan' in val.lower():
                                _v = val.split('|')
                                # hp
                                if 'percent' in _v[2].strip():
                                    fanlist.append(_v[0])
                                # lenvov & ibm & dell
                                elif 'RPM' in _v[2].strip():
                                    fanlist.append(_v[0])
                                else:
                                    continue
                            fan_num = len(fanlist)
                        if not fan_num:
                            fan_num='unsupported'
                    else:
                        fan_num='unsupported'
                else:
                    fan_num='failed (command get fan)'

                #cpu info
                cpu_num=''
                cpu = self.get_data("sensor list | grep -E -i 'CPU'")
                if cpu['status'] == 1:
                    if cpu['msg']:
                        cpulist=[]
                        for val in cpu['msg'].splitlines():
                            if 'cpu' in val.lower():
                                _v =  val.split('|')
                                if 'degrees' in _v[2].strip():
                                    cpulist.append(_v[0])
                                else:
                                    continue
                        cpu_num = len(cpulist)
                        if not cpu_num:
                            cpu_num = 'unsupported'
                    else:
                        cpu_num='unsupported'
                else:
                    cpu_num='failed (command get fan)'

                # mem info
                mem_num=''
                mem = self.get_data("sensor list | grep -E -i 'DIMM'")
                if mem['status'] == 1:
                    if mem['msg']:
                        memlist=[]
                        for val in mem['msg'].splitlines():
                            if 'DIMM' in val:
                                _v = val.split('|')
                                if 'degrees' in _v[2].strip():
                                    memlist.append(_v[0])
                                else:
                                    continue
                        mem_num= len(memlist)
                        if not mem_num:
                            mem_num='unsupported'
                    else:
                        mem_num='unsupported'
                else:
                    mem_num='failed (command get mem)'

                # net info
                net_json=''
                net = self.get_data("lan print | grep -E -i 'address|mask'")
                if net['status'] == 1:
                    if net['msg']:
                        net_dict = {}
                        for val in net['msg'].splitlines():
                            if ('address' or 'mask') in val.lower():
                                _v = val.split(': ')
                                _k = _v[0].strip()
                                net_dict[''.join(_k.split())] = _v[1].strip()
                        if not net_dict:
                            net_json='unsupported'
                        else:
                            net_json=net_dict
                    else:
                        net_json='unsupported'
                else:
                    net_json='failed (command get net)'

            return {'uuid':uuid_data,'fw':fw_data,'fan_num':fan_num,
                    'cpu_num':cpu_num,'mem_num':mem_num,'net':net_json,
                    'hd':hd}
        else:
            return {'error':'get ipmi data faild'}

# operation power
    def oper_power(self,action):
        res = self.get_data("power " + action)
        return res

# status
    def get_status(self):
        hd = self.get_fru()
        brand=hd['brand']
        if 'dell' in brand.lower():
            #cpu
            cpu_data = {}
            cpu_temp=[]
            cpu_temp_info = self.get_data("sensor list | grep -E -i 'Temp'")

            if cpu_temp_info['status'] == 1:
                if cpu_temp_info['msg']:
                    for val in cpu_temp_info['msg'].splitlines():
                        _v = val.split('|')
                        if 'degrees' in _v[2].strip():
                            cpu_temp.append(float(_v[1].strip()))
                        else:
                            continue
                    if not cpu_temp:
                        cpu_temp_avg ='unsupported'
                    else:
                        cpu_temp_avg = '%.2f' %(sum(cpu_temp) / len(cpu_temp))
                else:
                    cpu_temp_avg ='unsupported'
            else:
                cpu_temp_avg ='failed (command get cpu temp)'

            cpu_sta_info = self.get_data("sensor list | grep -E -i 'CPU Usage'")
            if cpu_sta_info['status']==1:
                if cpu_sta_info['msg']:
                    cpu_sta = cpu_sta_info['msg'].split('|')[3].strip()
                else:
                    cpu_sta = 'unsupported'
            else:
                cpu_sta = 'failed (command get cpu use)'

            cpu_data['temp']=cpu_temp_avg
            cpu_data['status']=cpu_sta

            #memory
            mem_data = {}
            mem_temp = []
            mem_info = self.get_data("sensor list | grep -E -i 'MEM Usage'")
            if mem_info['status']==1:
                if mem_info['msg']:
                    mem_sta = mem_info['msg'].split('|')[3].strip()
                else:
                    mem_sta = 'unsupported'
            else:
                mem_sta = 'faild (command get mem sta)'
            mem_temp = 'unsupported'
            mem_data['temp']=mem_temp
            mem_data['status']=mem_sta

            #fan
            fan_data = {}
            fan_sta=[]
            fan_temp=[]
            fan = self.get_data("sensor list | grep -E -i 'fan'")
            if fan['status'] == 1:
                if fan['msg']:
                    for val in fan['msg'].splitlines():
                        _v = val.split('|')
                        if 'RPM' in _v[2].strip():
                            fan_temp.append(float(_v[1].strip()))
                            fan_sta.append(_v[3].strip())
                        else:
                            continue
                    if len(set(fan_sta)) >= 2:
                        fan_data['status'] = 'issue'
                    else:
                        fan_data['status'] = 'ok'
                    fan_temp_avg = '%.2f' %(sum(fan_temp) / len(fan_temp))
                    if float(fan_temp_avg) > 100:
                        unit = ' RPM'
                    else:
                        unit = ' %'
                    fan_data['turn']=fan_temp_avg + unit
                else:
                    fan_data['status'] = 'unsupported'
                    fan_data['turn'] = 'unsupported'
            else:
                fan_data['status'] = 'faild (command get fan sta)'
                fan_data['turn'] = 'faild (command get fan turn)'

            #power
            power_data={}
            power_watts_info = self.get_data("sensor list | grep -E -i 'Pwr Consumption'")

            if power_watts_info['status']==1:
                if power_watts_info['msg']:
                    power_watts = power_watts_info['msg'].split('|')[1].strip()
                    power_status = power_watts_info['msg'].split('|')[3].strip()
                    power_data['watts']=power_watts
                    power_data['status']=power_status
                else:
                    power_data['watts']='unsupported'
                    power_data['status']='unsupported'
            else:
                power_data['watts']='faild (command get power watts)'
                power_data['status']='faild (command get power sta)'
        else:
            #cpu
            cpu_data = {}
            cpu = self.get_data("sensor list | grep -E -i 'CPU'")
            if cpu['status']==1:
                if cpu['msg']:
                    cpu_temp=[]
                    cpu_sta=[]
                    for val in cpu['msg'].splitlines():
                        _v =  val.split('|')
                        if 'degrees' in _v[2].strip():
                            cpu_temp.append(float(_v[1].strip()))
                            cpu_sta.append(_v[3].strip())
                        else:
                            continue
                    if len(set(cpu_sta)) >= 2:
                        cpu_data['status'] = 'issue'
                    else:
                        cpu_data['status'] = 'ok'
                    cpu_temp_avg = '%.2f' %(sum(cpu_temp) / len(cpu_temp))
                    cpu_data['temp']=cpu_temp_avg
                else:
                    cpu_data['status'] = 'unsupported'
                    cpu_data['temp']='unsupported'
            else:
                cpu_data['status'] = 'faild (command get cpu status)'
                cpu_data['temp']='faild (command get cpu temp)'

            # memory
            mem_data = {}
            mem_sta = []
            mem_temp = []
            mem = self.get_data("sensor list | grep -E -i 'DIMM'")
            if mem['status']==1:
                if mem['msg']:
                    for val in mem['msg'].splitlines():
                        _v = val.split('|')
                        if 'degrees' in _v[2].strip():
                            mem_temp.append(float(_v[1].strip()))
                            mem_sta.append(_v[3].strip())
                        else:
                            continue
                    if len(set(mem_sta)) >= 2:
                        mem_data['status'] = 'issue'
                    else:
                        mem_data['status'] = 'ok'
                    mem_temp_avg = '%.2f' %(sum(mem_temp) / len(mem_temp))
                    mem_data['temp']=mem_temp_avg
                else:
                    mem_data['status'] = 'unsupported'
                    mem_data['temp']='unsupported'
            else:
                mem_data['status'] = 'faild (command get mem status)'
                mem_data['temp']='faild (command get mem temp)'

            #fans
            fan_data = {}
            fan_sta=[]
            fan_temp=[]
            fan = self.get_data("sensor list | grep -E -i 'fan'")
            if fan['status'] ==1:
                if fan['msg']:
                    for val in fan['msg'].splitlines():
                        _v = val.split('|')
                    # hp
                        if 'percent' in _v[2].strip():
                            fan_temp.append(float(_v[1].strip()))
                            fan_sta.append(_v[3].strip())
                    # lenvov ibm
                        elif 'RPM' in _v[2].strip():
                            fan_temp.append(float(_v[1].strip()))
                            fan_sta.append(_v[3].strip())

                    if len(set(fan_sta)) >= 2:
                        fan_data['status'] = 'issue'
                    else:
                        fan_data['status'] = 'ok'
                    fan_temp_avg = '%.2f' %(sum(fan_temp) / len(fan_temp))
                    if float(fan_temp_avg) > 100:
                        unit = ' RPM'
                    else:
                        unit = ' %'
                    fan_data['turn']=fan_temp_avg + unit
                else:
                    fan_data['status'] = 'unsupported'
                    fan_data['turn'] = 'unsupported'
            else:
                fan_data['status'] = 'faild (command get fan sta)'
                fan_data['turn'] = 'faild (command get fan turn)'



            #power
            power_data = {}
            power = self.get_data("sensor list | grep -E -i power")
            if power['status']==1:
                if power['msg']:
                    for val in power['msg'].splitlines():
                        _v = val.split('|')
                    #lenovo
                        if 'Power Reading' in _v[0]:
                            power_data['watts'] = _v[1].strip()
                            power_data['status'] = _v[3].strip()
                    #hp
                        elif 'Power Meter' in _v[0]:
                            power_data['watts'] = _v[1].strip()
                            power_data['status'] = _v[3].strip()
                    #IBM
                        elif 'Avg Power' in _v[0]:
                            power_data['watts'] = _v[1].strip()
                            power_data['status'] = _v[3].strip()
                else:
                    power_data['watts']='unsupported'
                    power_data['status']='unsupported'
            else:
                power_data['watts']='faild (command get power watts)'
                power_data['status']='faild (command get power sta)'

        #return json.dumps(mem_sta)
        return {
            'cpu_sta':json.dumps(cpu_data),
            'mem_sta':json.dumps(mem_data),
            'fan_sta':json.dumps(fan_data),
            'power_sta':json.dumps(power_data),
        }

# uuid
    def get_uuid(self):
        #uuid_data={}
        uuid = self.get_data('mc guid | grep -i GUID')
        for val in uuid['msg'].splitlines():
            _v=val.split(':')
            if len(_v) != 2:
                continue
            uuid_data=_v[1].strip()

            return (uuid_data)


if __name__ == "__main__":
    #ipmi_login = ipmi_api('192.168.3.11', 'administrator', '123qweASD')
    ipmi_login = ipmi_api('192.168.1.14', 'root', '123qweASD')
    info = ipmi_login.get_info()

    print(info)
