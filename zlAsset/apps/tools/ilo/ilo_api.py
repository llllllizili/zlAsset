# coding: utf-8
import sys
import hpilo
import re
import json
import time
import signal

class IloApi():
    def __init__(self,username,password,server,**kwargs):
        self.username=username
        self.password=password
        self.server=server
        self.ssl=kwargs.get('ssl','')
        self.ilo=''

    # def signal_handler(self,signum,frame):
    #     exit('Timeout')

    def login(self):
        # signal.signal(signal.SIGALRM,self.signal_handler)
        # signal.alarm(10)
        self.ilo = hpilo.Ilo(self.server,self.username,self.password)
        try:
            self.ilo.get_fw_version()
        except Exception as e:
            return {'status':0,'msg':e}

        return {'status':1,'msg':'login ok'}

    def get_HD(self):
        self.login
        uuid=''
        sn=''
        product_name=''
        cpu = ''
        cores=0
        mem=0
        disk=0
        _mac=[]
        raid_level=None
        _disk_detail={}
        _mem_detail={}
        _cpu_detail={}
        _source={}
        _fwversion = {}
        BoardManufactureDateTime=''
        ChassisType=''


        try:

            ret = self.ilo.get_host_data(decoded_only=True)

            health_data=self.ilo.get_embedded_health()

            _source=health_data

            for k,v in health_data.items():

                if k == 'storage':
                    disk=re.sub('[A-Za-z]','',v['Controller on System Board']['logical_drives'][0]['capacity']).strip()
                    raid_level=re.sub('[A-Za-z]','',v['Controller on System Board']['logical_drives'][0]['fault_tolerance']).strip()

                    _disk_detail=v['Controller on System Board']['logical_drives'][0]['physical_drives']

                if k == 'memory':
                    _mem_detail=v
                    pass

                if k == 'processors':

                    _cpu_detail=v
                    pass

                if k=='firmware_information':
                    _fwversion = v
                    pass


                pass

            #logger.debug(ret)
            for val in ret:


                # if val.has_key('Date'):
                if 'Date' in val:
                    BoardManufactureDateTime=val['Date']

                # if val.has_key('UUID'):
                if 'UUID' in val:
                    sn=val['Serial Number']
                    product_name=val['Product Name']

                #elif val.has_key('Memory Technology'):
                elif 'Memory Technology' in val:
                    cpu += val['Execution Technology'] +' '+ val['Speed']+';'
                    _cores = re.sub('threads',"",re.sub('.*;',"",val['Execution Technology'])).strip()
                    cores +=int(_cores)

                #elif val.has_key('Size'):
                elif 'Size' in val:
                    if val['Size']=='not installed':
                        pass
                    else:
                        mem +=int(val['Size'].strip('MB').strip())

                #elif val.has_key('cUUID'):
                elif 'cUUID' in val:
                    uuid=val['cUUID']

                #elif val.has_key('Port'):
                elif 'Port' in val:
                    _mac.append({'mac':val['MAC'].replace('-',':'),'port':str(val['Port'])})

        except Exception as e:
            raise e

        return {'uuid':uuid,'sn':sn,'product_name':product_name,'cpu':cpu,'cores':cores,'mem':int(mem/1024),'mac':_mac,'disk':disk,'disk_detail':json.dumps(_disk_detail),
                'mem_detail':json.dumps(_mem_detail),'BoardManufactureDateTime':BoardManufactureDateTime,'ChassisType':ChassisType,'_source':json.dumps(_source),
                'cpu_detail':json.dumps(_cpu_detail),'fw':json.dumps(_fwversion)}

    def get_L(self):
        pass
    def get_H(self):
        pass

    def get_mem(self):
        mem_list = []
        mem_set = []
        subkey = ['type','frequency','size']

        mem_info= {}
        _ret = self.get_HD()
        _source = json.loads( _ret['_source'])
        memory = _source['memory']['memory_details']

        #save data --- list
        for k,v in memory.items():
            for kk,vv in v.items():
                subdict=dict([(key, vv[key]) for key in subkey])
                mem_list.append(subdict)

        # set list
        for i in mem_list:
            if i not in mem_set:
                mem_set.append(i)

        for j in mem_set:
            mem_info[mem_list.count(j)]=j

        return mem_info



    def get_log(self):
        ilo_log = {}
        log = self.ilo.get_ilo_event_log()
        for i,d in enumerate(log):
            if d['severity'] == 'Informational':
                continue
            else:
                ilo_log[i] = d

        return ilo_log
            #for val in d:
             #   print val['severity']

    def get_license(self):
        license  = self.ilo.get_all_licenses()
        license_key = license[0].get("license_key")
        return license_key

    def get_info(self):
        _ret = self.get_HD()
        _source = json.loads( _ret['_source'])
        net = _source['nic_information']
        fw = json.loads(_ret['fw'])
        cpu_slot = len(_source['processors'])
        disk = _source['storage']['Controller on System Board']
        disk_logical=disk['logical_drives']
        fans = _source['fans']
        power = _source['power_supplies']
        memory = _source['memory']['memory_details']

        mem_detail = json.loads( _ret['mem_detail'])


        def get_mem():
            mem_info= {}
            mem_list = []
            mem_set = []
            subkey = ['type','frequency','size']

            #save data --- list
            for k,v in memory.items():
                for kk,vv in v.items():
                    subdict=dict([(key, vv[key]) for key in subkey])
                    mem_list.append(subdict)

            # set list
            for i in mem_list:
                if i not in mem_set:
                    mem_set.append(i)

            for j in mem_set:
                mem_info[mem_list.count(j)]=j

            return mem_info


        def get_mac():
            net_mac={}
            for k,v in net.items():
                net_mac[''.join(k.split())] = v['mac_address']

            return net_mac

        def get_cpu():
            cpu_info={}
            for i in range(1,cpu_slot+1):
                cpu_info['cpu_' + str(i)] = _source['processors']['Proc ' + str(i)]['name']
            cpu_info['cpu_core'] = (_ret['cpu'])
            cpu_info['cpu_slot'] = cpu_slot
            return cpu_info

        def get_disk():
            disk_info={}

            for i in range(len(disk_logical)):
                disk_info[i]={}
                disk_info[i]['capacity'] = disk_logical[i]['capacity']
                disk_info[i]['label'] = disk_logical[i]['physical_drives'][0]['label']

            return disk_info

        def get_raid():
            raid_info={}
            raid_info['raid_type'] = disk_logical[1]['fault_tolerance']
            raid_info['raid_model'] = disk['model']

            return json.dumps(raid_info)

        def get_power_type():
            status = []
            power_num = len(power)
            for v in power:
                status.append(power[v]['status'])
            if power_num >= 2:
                g = status.count('Good')
                if g >=2:
                    sta = 'Redundant'
                    return sta
                else:
                    sta = 'Single-Point'
                    return sta

        def get_power_watt():
            p_sum = _source['power_supply_summary']
            for v in p_sum:
                watts = p_sum['present_power_reading']
            return watts

        def get_fan_speed():
            fan_list = []
            for k,v in fans.items():
                fan_list.append(v['speed'][0])
            fan_num = len(fan_list)
            speed_avg = ('%.2f' %(sum(fan_list) / fan_num))

            return speed_avg +'%'

        info = dict(
                uuid = (_ret['uuid']),
                sn = (_ret['sn']).strip(),
                product_name = (_ret['product_name']),
                net_num = len(net),
                net_mac = get_mac(),
                fw_ver = fw['iLO'],
                cpu_info = get_cpu(),
                disk_info = get_disk(),
                raid_info = get_raid(),
                #fan_speed = get_fan_speed(),
                power_type = get_power_type(),
                #spower_watt = get_power_watt(),
                #ilo_log = self.get_log(),
                mem = get_mem(),
                license=self.get_license(),
            )
        return info


    def get_status(self):
        sta_dict = {}
        _ret = self.get_HD()
        _source = json.loads( _ret['_source'])
        sta= _source['health_at_a_glance']
        fans = _source['fans']
        power = _source['power_supplies']

        def get_power_watt():
            p_sum = _source['power_supply_summary']
            for v in p_sum:
                watts = p_sum['present_power_reading']
            return watts

        def get_fan_speed():
            fan_list = []
            for k,v in fans.items():
                fan_list.append(v['speed'][0])
            fan_num = len(fan_list)
            speed_avg = ('%.2f' %(sum(fan_list) / fan_num))

            return speed_avg +'%'

        for k,v in sta.items():
            sta_dict[k] = v['status']

        sta_dict['fan_speed'] = get_fan_speed()
        sta_dict['power_watt'] = get_power_watt()

        return sta_dict



    def discovery_search(self):
        info={}
        # signal.signal(signal.SIGALRM,self.signal_handler)
        # signal.alarm(10)
        self.login
        ret = self.ilo.get_host_data(decoded_only=True)
        for val in ret:
            if val.has_key('UUID'):
                info['sn']=val['Serial Number'].strip()
                info['model']=val['Product Name']

        return info
