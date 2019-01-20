#/bin/bash
check_os_release(){
  while true
  do
    os_release=$(grep "Red Hat Enterprise Linux Server release" /etc/issue 2>/dev/null)
    os_release_2=$(grep "Red Hat Enterprise Linux Server release" /etc/redhat-release 2>/dev/null)
    if [ "$os_release" ] && [ "$os_release_2" ]
    then
      if echo "$os_release"|grep "release 5" >/dev/null 2>&1
      then
        os_release=redhat5
        echo "$os_release"
      elif echo "$os_release"|grep "release 6" >/dev/null 2>&1
      then
        os_release=redhat6
        echo "$os_release"
      elif echo "$os_release"|grep "release 7" >/dev/null 2>&1
      then
        os_release=redhat7
        echo "$os_release"
      else
        os_release=""
        echo "$os_release"
      fi
      break
    fi
    os_release=$(grep "Aliyun Linux release" /etc/issue 2>/dev/null)
    os_release_2=$(grep "Aliyun Linux release" /etc/aliyun-release 2>/dev/null)
    if [ "$os_release" ] && [ "$os_release_2" ]
    then
      if echo "$os_release"|grep "release 5" >/dev/null 2>&1
      then
        os_release=aliyun5
        echo "$os_release"
      elif echo "$os_release"|grep "release 6" >/dev/null 2>&1
      then
        os_release=aliyun6
        echo "$os_release"
      elif echo "$os_release"|grep "release 7" >/dev/null 2>&1
      then
        os_release=aliyun7
        echo "$os_release"
      else
        os_release=""
        echo "$os_release"
      fi
      break
    fi
    os_release_2=$(grep "CentOS" /etc/*release 2>/dev/null)
    if [ "$os_release_2" ]
    then
      if echo "$os_release_2"|grep "release 5" >/dev/null 2>&1
      then
        os_release=centos5
        echo "$os_release"
      elif echo "$os_release_2"|grep "release 6" >/dev/null 2>&1
      then
        os_release=centos6
        echo "$os_release"
      elif echo "$os_release_2"|grep "release 7" >/dev/null 2>&1
      then
        os_release=centos7
        echo "$os_release"
      else
        os_release=""
        echo "$os_release"
      fi
      break
    fi
    os_release=$(grep -i "ubuntu" /etc/issue 2>/dev/null)
    os_release_2=$(grep -i "ubuntu" /etc/lsb-release 2>/dev/null)
    if [ "$os_release" ] && [ "$os_release_2" ]
    then
      if echo "$os_release"|grep "Ubuntu 10" >/dev/null 2>&1
      then
        os_release=ubuntu10
        echo "$os_release"
      elif echo "$os_release"|grep "Ubuntu 12.04" >/dev/null 2>&1
      then
        os_release=ubuntu1204
        echo "$os_release"
      elif echo "$os_release"|grep "Ubuntu 12.10" >/dev/null 2>&1
      then
        os_release=ubuntu1210
        echo "$os_release"
     elif echo "$os_release"|grep "Ubuntu 14.04" >/dev/null 2>&1
     then
        os_release=ubuntu1204
        echo "$os_release"
      else
        os_release=""
        echo "$os_release"
      fi
      break
    fi
    os_release=$(grep -i "debian" /etc/issue 2>/dev/null)
    os_release_2=$(grep -i "debian" /proc/version 2>/dev/null)
    if [ "$os_release" ] && [ "$os_release_2" ]
    then
      if echo "$os_release"|grep "Linux 6" >/dev/null 2>&1
      then
        os_release=debian6
        echo "$os_release"
      elif echo "$os_release"|grep "Linux 7" >/dev/null 2>&1
      then
        os_release=debian7
        echo "$os_release"
      else
        os_release=""
        echo "$os_release"
      fi
      break
    fi
    break
    done
}

os_release=$(check_os_release)

#磁盘使用情况
get_disk(){
  DEV=`df -hP | grep '^/dev/*' | cut -d' ' -f1 | sort`
  for I in $DEV
  do
    dev=`df -Ph | grep $I | awk '{print $1}'`
    size=`df -Ph | grep $I | awk '{print $2}'`
    used=`df -Ph | grep $I | awk '{print $3}'`
    free=`df -Ph | grep $I | awk '{print $4}'`
    rate=`df -Ph | grep $I | awk '{print $5}'`
    mount=`df -Ph | grep $I | awk '{print $6}'`
    #echo -e "$I:\tsize:$size\tused:$used\tfree:$free\trate:$rate\tmount:$mount"
    echo -e "'$I':{'size':'$size','used':'$userd','free':'$free'},"
  done
}

#获取centos信息
get_centos_info(){
  os_sys=`uname -o`
  os_version=`cat /etc/redhat-release`
  os_kernel=`uname -r`
  cpu_model=`grep 'model name' /proc/cpuinfo |uniq |awk -F : '{print $2}'`
  cpu_num=`cat /proc/cpuinfo| grep 'physical id'| sort| uniq| wc -l`
  cpu_core=`grep 'cpu cores' /proc/cpuinfo |uniq |awk -F : '{print $2}'`
  cpu_load=`cat /proc/loadavg | awk '{print $1}'`
  #mem_total=`free -m |grep -i mem |awk '{ print $2}'` #系统总内存,与物理不符,因为系统初始化会保留一部分内存
  mem_total=(`dmidecode -t memory | grep 'Installed Size' | awk -F : 'NR==1{ print $2 }'`) #物理总内存
  mem_used=`free -m |grep -i mem |awk '{print ($3-$6)/$2*100,"%"}'`
  #mem_used=`free -m |grep -i mem |awk '{print ($3-$6-$7)/$2*100,"%"}'` redhat
  disk_total=`lsblk | grep -E -i 'disk|磁盘' | grep -E -i 'sd|vd' | awk '{ print $4 }'`

#dict
  echo "{\
  'os_sys':$os_sys\
  'os_version':'$os_version',\
  'os_kernel':'$os_kernel',\
  'cpu_model':'$cpu_model',\
  'cpu_num':'$cpu_num'\
  'cpu_core':'$cpu_core'\
  'cpu_load':'$cpu_load',\
  'mem_total':'$mem_total',\
  'mem_used':'$mem_used',\
  'disk_total':'$disk_total',\
  }"
}

#获取redhat信息
get_redhat_info(){
  echo 'redaht'
}


#获取ubuntu信息
get_ubuntu_info(){
  echo 'ubuntu'
}

#判断系统返回结果
if [[ $os_release =~ 'centos' ]]
then
  centos_info=$(get_centos_info)
  echo $centos_info
fi
