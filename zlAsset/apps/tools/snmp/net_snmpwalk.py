# coding: utf-8
# authour: zili
import commands
import re
import sys
from collections import defaultdict
import json

WALK_CMD='snmpwalk'

class WalkApi(object):
    def __init__(self,comm,ver,ip):
        self.comm  = comm
        self.ver = ver 
        self.ip = ip

    def get_data(self,oid):
        (status,output) = commands.getstatusoutput(WALK_CMD + ' -c '+self.comm+' -v '+self.ver+' '+self.ip +' '+ oid)
        if status >0:
            return {'status':0,'msg':output}
        else:
            return {'status':1,'msg':output}

#if ret['status'] == 1:
    def sysDescr(self):
        data = self.get_data('1.3.6.1.2.1.1.1.0')
        if 'Timeout' in data['msg']:
            return 'Timeout: No Response from ' + self.ip
        if 'No Such Instance' in data['msg']:
            return {'error':'No Such Instance currently exists at this OID'}
        try:
            res = data['msg']
            res_i = res.split('=')

            netsysdescr={}
            val = res_i[1].split(':')[1]

            if 'h3c' in val.lower():
                netsysdescr['brand'] = 'H3C'
                netsysdescr['version']=re.compile('Version(.*), R').findall(val)[0]
                netsysdescr['model']=re.compile('H3C(.*)So').findall(val)[0]
            elif 'cisco' in val.lower():
                netsysdescr['brand'] = 'CISCO'
                netsysdescr['version']=re.compile('Version(.*), R').findall(val)[0]
                netsysdescr['model']=re.compile('Software (.*), V').findall(val)[0]
            elif 'cisco' in val.lower() and 'security' in val.lower():
                netsysdescr['brand'] = 'CISCO ASA'
                netsysdescr['version']=re.compile('Version(.*)').findall(val)[0]
                netsysdescr['model']='unsupported'
            elif 'cisco' in val.lower() and 'controller' in val.lower():
                netsysdescr['brand'] = 'CISCO Controller'
                netsysdescr['version']='unsupported'
                netsysdescr['model']='unsupported'
            elif 'linux ns' in val.lower():
                netsysdescr['brand'] = 'netentsec'
                netsysdescr['version']=re.compile('NS (.*)-').findall(val)[0]
                netsysdescr['model']=re.compile('-(.*) #').findall(val)[0]
            elif 'dell' in val.lower() and 'networking' in val.lower():
                netsysdescr['brand'] = 'DELL'
                netsysdescr['version']=re.compile(',(.*),').findall(val)[0]
                netsysdescr['model']=re.compile('Networking (.*),').findall(val)[0]
            elif 'ds' in val.lower():
                netsysdescr['brand'] = 'EMC'
                netsysdescr['version']='unsupported'
                netsysdescr['model']=val
            else:
                netsysdescr['brand'] = 'unsupported'
                netsysdescr['version']='unsupported'
                netsysdescr['model']='unsupported'

            return  netsysdescr
        except Exception, e:
            return {'error':str(e)}

    def sysUptime(self):
        data = self.get_data('1.3.6.1.2.1.1.3.0')
        if 'No Such Instance' in data['msg']:
            return {'error':'No Such Instance currently exists at this OID'}
        else:
            try:
                res = data['msg']
                res_i = res.split('=')
                time = res_i[1].split(',')[0].split(':')[1]
                netsysuptime = re.findall(r'[(](.*?)[)]', time)
                return  {'netsysuptime':netsysuptime[0]}
            except Exception, e:
                return {'error':str(e)}

    def sysName(self):
        data = self.get_data('1.3.6.1.2.1.1.5.0')
        if 'No Such Instance' in data['msg']:
            return {'error':'No Such Instance currently exists at this OID'}
        else:
            try:
                res = data['msg']
                res_i = res.split('=')
                netsysname = res_i[1].split(':')[1]
                return  {'netsysname':netsysname}
            except Exception, e:
                return {'error':str(e)}

    # def sysLocation(self):
    #     data = self.get_data('1.3.6.1.2.1.1.6.0')
    #     if 'No Such Instance' in data['msg']:
    #         return {'error':'No Such Instance currently exists at this OID'}
    #     else:
    #         try:
    #             res = data['msg']
    #             res_i = res.split('=')
    #             netsyslocation = res_i[1].split(':')[1]
    #             return  {'netsyslocation':netsyslocation}
    #         except Exception, e:
    #             return {'error':str(e)}

    def ifIndex(self):
        data = self.get_data('1.3.6.1.2.1.2.2.1.1')
        if 'No Such Instance' in data['msg']:
            return {'error':'No Such Instance currently exists at this OID'}
        else:
            try:
                res = data['msg']
                res_i = res.split('\n')
                data_dict={}
                for i in res_i:
                    res_ii = i.split('=')
                    key = res_ii[0].split('.')[1].strip()
                    val = res_ii[1].split(':')[1].strip()
                    data_dict[key]=val
                return  data_dict
            except Exception, e:
                return {'error':str(e)}
#端口描述
    def ifDescr(self):
        data = self.get_data('1.3.6.1.2.1.2.2.1.2')
        if 'No Such Instance' in data['msg']:
            return {'error':'No Such Instance currently exists at this OID'}
        else:
            try:
                res = data['msg']
                res_i = res.split('\n')
                data_dict={}
                for i in res_i:
                    res_ii = i.split('=')
                    key = res_ii[0].split('.')[1].strip()
                    val = res_ii[1].split(':')[1].strip()
                    data_dict[key]=val
                return  data_dict
            except Exception, e:
                return {'error':str(e)}

#mtu
    def ifMtu(self):
        data = self.get_data('1.3.6.1.2.1.2.2.1.4')
        if 'No Such Instance' in data['msg']:
            return {'error':'No Such Instance currently exists at this OID'}
        else:
            try:
                res = data['msg']
                res_i = res.split('\n')
                data_dict={}
                for i in res_i:
                    res_ii = i.split('=')
                    key = res_ii[0].split('.')[1].strip()
                    val = res_ii[1].split(':')[1].strip()
                    data_dict[key]=val
                return  data_dict
            except Exception, e:
                return {'error':str(e)}
#速率
    def ifSpeed(self):
        data = self.get_data('1.3.6.1.2.1.2.2.1.5')
        if 'No Such Instance' in data['msg']:
            return {'error':'No Such Instance currently exists at this OID'}
        else:
            try:
                res = data['msg']
                res_i = res.split('\n')
                data_dict={}
                for i in res_i:
                    res_ii = i.split('=')
                    key = res_ii[0].split('.')[1].strip()
                    val = res_ii[1].split(':')[1].strip()
                    data_dict[key]=val
                return  data_dict
            except Exception, e:
                return {'error':str(e)}

#mac地址
    def ifPhysAddress(self):
        data = self.get_data('1.3.6.1.2.1.2.2.1.6')
        if 'No Such Instance' in data['msg']:
            return {'error':'No Such Instance currently exists at this OID'}
        else:
            try:
                res = data['msg']
                res_i = res.split('\n')
                data_dict={}
                for i in res_i:
                    res_ii = i.split('=')
                    key = res_ii[0].split('.')[1].strip()
                    val = res_ii[1].split(' ')[2].strip()
                    data_dict[key]=val
                return  data_dict
            except Exception, e:
                return {'error':str(e)}
#端口状态
    def ifAdminStatus(self):
        data = self.get_data('1.3.6.1.2.1.2.2.1.7')
        if 'No Such Instance' in data['msg']:
            return {'error':'No Such Instance currently exists at this OID'}
        else:
            try:
                
                res = data['msg']
                res_i = res.split('\n')
                data_dict={}
                for i in res_i:
                    res_ii = i.split('=')
                    key = res_ii[0].split('.')[1].strip()
                    val = res_ii[1].split(':')[1].strip()
                    data_dict[key]=val
                return  data_dict
            except Exception, e:
                return {'error':str(e)}

#端口管理状态
    def ifOperStatus(self):
        data = self.get_data('1.3.6.1.2.1.2.2.1.8')
        if 'No Such Instance' in data['msg']:
            return {'error':'No Such Instance currently exists at this OID'}
        else:
            try:
                res = data['msg']
                res_i = res.split('\n')
                data_dict={}
                for i in res_i:
                    res_ii = i.split('=')
                    key = res_ii[0].split('.')[1].strip()
                    val = res_ii[1].split(':')[1].strip()
                    data_dict[key]=val
                return  data_dict
            except Exception, e:
                return {'error':str(e)}

#端口描述
    def ifAlias(self):
        data = self.get_data('1.3.6.1.2.1.31.1.1.1.18')
        if 'No Such Instance' in data['msg']:
            return {'error':'No Such Instance currently exists at this OID'}
        else:
            try:
                res = data['msg']
                res_i = res.split('\n')
                data_dict={}
                for i in res_i:
                    res_ii = i.split('=')
                    key = res_ii[0].split('.')[1].strip()
                    val = res_ii[1].split(':')[1].strip()
                    data_dict[key]=val
                return  data_dict
            except Exception, e:
                return {'error':str(e)}
#管理先关
    def ipAdEntAddr(self):
        data = self.get_data('1.3.6.1.2.1.4.20.1.1')
        if 'No Such Instance' in data['msg']:
            return {'error':'No Such Instance currently exists at this OID'}
        else:
            try:
                res = data['msg']
                res_i = res.split('\n')
                data_list=[]
                for i in res_i:
                    res_ii = i.split('=')
                    val = res_ii[1].split(':')[1].strip()
                    data_list.append(val)
                return  data_list
            except Exception, e:
                return {'error':str(e)}

    def ipAdEntIfIndex(self):
        data = self.get_data('1.3.6.1.2.1.4.20.1.2')
        if 'No Such Instance' in data['msg']:
            return {'error':'No Such Instance currently exists at this OID'}
        else:
            try:
                
                res = data['msg']
                res_i = res.split('\n')
                data_dict={}
                for i in res_i:
                    res_ii = i.split('=')
                    key = res_ii[0].split('.')
                    ip = '.'.join([key[1],key[2],key[3],key[4]])
                    val = res_ii[1].split(':')[1].strip()
                    data_dict[ip]=val
                return  data_dict
            except Exception, e:
                return {'error':str(e)}

    def ipAdEntNetMask(self):
        data = self.get_data('1.3.6.1.2.1.4.20.1.3')
        if 'No Such Instance' in data['msg']:
            return {'error':'No Such Instance currently exists at this OID'}
        else:
            try:
                
                res = data['msg']
                res_i = res.split('\n')
                data_dict={}
                for i in res_i:
                    res_ii = i.split('=')
                    key = res_ii[0].split('.')
                    ip = '.'.join([key[1],key[2],key[3],key[4]])
                    val = res_ii[1].split(':')[1].strip()
                    data_dict[ip]=val
                return  data_dict
            except Exception, e:
                return {'error':str(e)}

    def ipNetToMediaIfindex(self):
        data = self.get_data('1.3.6.1.2.1.4.22.1.1')
        if 'No Such Instance' in data['msg']:
            return {'error':'No Such Instance currently exists at this OID'}
        else:
            try:
                
                res = data['msg']
                res_i = res.split('\n')
                data_dict={}
                for i in res_i:
                    res_ii = i.split('=')
                    key = res_ii[0].split('.')
                    ip = '.'.join([key[2],key[3],key[4],key[5]]).strip()
                    val = res_ii[1].split(':')[1].strip()
                    data_dict[ip]=val
                return  data_dict
            except Exception, e:
                return {'error':str(e)}


    def ipNetToMediaPhysAddress(self):
        data = self.get_data('1.3.6.1.2.1.4.22.1.2')
        if 'No Such Instance' in data['msg']:
            return {'error':'No Such Instance currently exists at this OID'}
        else:
            try:
                res = data['msg']
                res_i = res.split('\n')
                data_dict={}
                for i in res_i:
                    res_ii = i.split('=')
                    key = res_ii[0].split('.')
                    ip = '.'.join([key[2],key[3],key[4],key[5]]).strip()
                    val = res_ii[1].split(' ')[2].strip()
                    mac = val.replace(":", "");
                    data_dict[ip]=mac
                return  data_dict
            except Exception, e:
                return {'error':str(e)}

    def get_info(self):
        sysDescr = self.sysDescr()
        if 'Timeout' in sysDescr:
            return {'error':'Timeout: No Response from '+self.ip}
        else:
            sysUptime = self.sysUptime()
            sysName = self.sysName()
            # sysLocation = self.sysLocation()
            ifIndex = self.ifIndex()
            ipNetToMediaPhysAddress = self.ipNetToMediaPhysAddress()
            ifDescr = self.ifDescr()
            ifMtu = self.ifMtu()
            ifSpeed = self.ifSpeed()
            ifPhysAddress = self.ifPhysAddress()
            ifAdminStatus = self.ifAdminStatus()
            ifOperStatus = self.ifOperStatus()
            ifAlias = self.ifAlias()
            ipAdEntAddr = self.ipAdEntAddr()
            ipAdEntNetMask = self.ipAdEntNetMask()
            ipAdEntIfIndex = self.ipAdEntIfIndex()
            ipNetToMediaIfindex = self.ipNetToMediaIfindex()

            Tree = lambda: defaultdict(Tree)
            results = Tree()

            try:
                for portid in ifIndex:
                    if portid in ifDescr:
                        results['netinterfaces'][portid]['name'] = ifDescr[portid]
                    if portid in ifMtu:
                        results['netinterfaces'][portid]['mtu'] = ifMtu[portid]
                    if portid in ifSpeed:
                        results['netinterfaces'][portid]['speed'] = ifSpeed[portid]
                    if portid in ifPhysAddress:
                        results['netinterfaces'][portid]['mac'] = ifPhysAddress[portid]
                    if portid in ifAdminStatus:
                        results['netinterfaces'][portid]['adminstatus'] = ifAdminStatus[portid]
                    if portid in ifOperStatus:
                        results['netinterfaces'][portid]['operstatus'] = ifOperStatus[portid]
                    if portid in ifAlias:
                        results['netinterfaces'][portid]['description'] = ifAlias[portid]
                for key_ip,val_portid in ipNetToMediaIfindex.items():
                    if key_ip in ipNetToMediaPhysAddress:
                        results['netipto'][key_ip]['index'] = ipNetToMediaIfindex[key_ip]
                        results['netipto'][key_ip]['mac'] = ipNetToMediaPhysAddress[key_ip]


                results['netsysdescr']=sysDescr
                results['netsysuptime']=sysUptime
                # results['netsyslocation']=sysLocation
                results['netsysname']=sysName
                results['netall_ipv4_addresses']=ipAdEntAddr

                return  results
            except Exception, e:
                return e

if __name__ == '__main__':
    snmpwalk = WalkApi('jingkun','2c','192.168.1.1')
    res = snmpwalk.get_info()
    print json.dumps(res)