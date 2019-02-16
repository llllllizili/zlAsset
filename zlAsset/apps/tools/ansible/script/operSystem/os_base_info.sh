#!/bin/bash
check_os_release()
{
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
      elif echo "$os_release"|grep "Ubuntu 16.04" >/dev/null 2>&1
      then
        os_release=ubuntu1604
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

#网卡信息
get_net(){
  echo -e "[\c"
  DEV=`ip address |grep ^[0-9] |awk -F: '{print $2}' |sed "s/ //g" |grep '^[ebp]'`
  for I in $DEV
  do
    speed=`ethtool $I | grep "Speed" |awk -F: '{print $2}'`
    link=`ip address show $I | grep -E "UP|DOWN" | awk -F" " '{print $9}'`
    hwaddr=`ip address show $I | grep "link/" | sed 's/^[ \t]*//;s/[ \t]*$//' | awk -F" " '{print $2}'`
    ip=`ip address show $I | grep -w "inet" |sed "s/^[ \t]*//g" |awk -F" " '{print $2}'`
    subnet=`echo $ip | awk -F'/' '{print $2}'`
    gateway=`route | grep 'default' | grep $I | awk '{print $2}' `
    echo -e "{\"name\":\"$I\",\"speed\":\"$speed\",\"link\":\"$link\",\"mac\":\"$hwaddr\",\"ip\":\"$ip\",\"subnet\":\"$subnet\",\"gateway\":\"$gateway\"}"
  done | sed '$!s/$/,/'
  echo -e "]\c"
}

get_cpu(){
    i=0
    for id in `grep 'processor' /proc/cpuinfo |awk -F: '{print $2}'`;do
        i=$((i+1))
    done

    ii=0
    echo -e "[\c"
    cpu=`grep 'model name' /proc/cpuinfo |awk -F: '{print $2}'`
    echo "$cpu" | while read line;do
        ii=$((ii+1))
        if [ "$ii" == $i ];
        then
            echo -e "{\"id\":\"CPU$((ii-1))\",\"name\":\"$line\"}"
        else
            echo -e "{\"id\":\"CPU$((ii-1))\",\"name\":\"$line\"},"
        fi
    done
    echo -e "]\c"
}

#磁盘使用情况
get_disk(){
  echo -e "[\c"
    DEV=`df -hPl | grep '^/dev/*' | cut -d' ' -f1 | sort`
    for I in $DEV
    do
      dev=`df -TPhl | grep $I | awk '{print $1}'`
      dev_type=`df -TPhl | grep $I | awk '{print $2}'`
      size=`df -TPhl | grep $I | awk '{print $3}'`
      used=`df -TPhl | grep $I | awk '{print $4}'`
      free=`df -TPhl | grep $I | awk '{print $5}'`
      use_per=`df -TPhl | grep $I | awk '{print $6}'`
      mount=`df -TPhl | grep $I | awk '{print $7}'`
      #echo -e "{\"name\":\"$I\",\"dev_type\":\"$dev_type\",\"size\":\"$size\",\"used\":\"$used\",\"freespace\":\"$free\",\"use_per\":\"$use_per\",\"filesystem\":\"$mount\"}"
      echo -e "{\"dev_type\":\"$dev_type\",\"size\":\"$size\",\"used\":\"$used\",\"freespace\":\"$free\", \"filesystem\":\"$mount\"}"
    done | sed '$!s/$/,/'
  echo -e "]\c"
}

#获取 netsta信息
get_netstat(){
  local IFS=$'\n'
  local OLDIFS="$IFS"
  SERVER=`netstat -ntulpa | grep -E 'tcp|udp' |awk -F' ' '{print $1,$4,$5,$6,$7}'`
  echo -e "[\c"
  for line in $SERVER
    do
      #echo $line
      Protocol=`echo $line | grep ES | awk '{print $1}'`
      LocalAddr=`echo $line | grep ES | awk '{print $2}'|awk -F: '{print $(NF-1)}'`
      LocalPort=`echo $line | grep ES | awk '{print $2}'|awk -F: '{print $NF}'`
      ForeignAddr=`echo $line |grep ES | awk '{print $3}'|awk -F: '{print $(NF-1)}'`
      ForeignPort=`echo $line |grep ES | awk '{print $3}'|awk -F: '{print $NF}'`
      State=`echo $line |grep ES | awk '{print $4}'`
      PID=`echo $line |grep ES | awk '{print $5}'| awk -F'/' '{print $1}'`
      App=`echo $line |grep ES | awk '{print $5}'| awk -F'/' '{print $2}'`
      #Program=`echo $line | awk '{print $7}'| awk -F'/' '{print $2}'`
      if [ "$PID" = "" ]; then
          continue;
      else
         echo -e "{\"protocol\":\"$Protocol\",\"pid\":\"$PID\",\"localaddr\":\"$LocalAddr\",\"localport\":\"$LocalPort\",\"foreignaddr\":\"$ForeignAddr\",\"foreignport\":\"$ForeignPort\",\"state\":\"$State\"}"
      fi
    done | sed '$!s/$/,/'
  echo -e "]\c"
}

# suse grep -i "SUSE" /etc/SuSE-release
#获取centos信息
get_info(){
  os_sys=`uname -o`
  host_name=`hostname`
  product_id=`dmidecode -t 1 | grep Serial | awk -F ':' '{print $2}'`
  if [[ $os_release =~ 'ubuntu' ]];then
    os_version=`grep -i "ubuntu" /etc/issue | awk -F' ' '{print $1$2$3}'`
  elif [[ $os_release =~ 'centos' ]];then
    os_version=`cat /etc/redhat-release`
  elif [[ $os_release =~ 'redhat' ]];then
    os_version=`cat /etc/redhat-release`
  else
    os_version=`cat /etc/redhat-release`
  fi
  os_kernel=`uname -r`
  cpu_num=`cat /proc/cpuinfo| grep 'physical id'| sort| uniq| wc -l`
  cpu_core=`grep 'cpu cores' /proc/cpuinfo |uniq |awk -F : '{print $2}'`
  cpu_load=`cat /proc/loadavg | awk '{print $1}'`
  #mem_total=`free -m |grep -i mem |awk '{ print $2}'`
  #系统总内存,与物理不符,因为系统初始化会保留一部分内存
  mem_total=(`dmidecode -t memory | grep 'Installed Size' | awk -F : 'NR==1{ print $2 }'`)
  #disk_total=`lsblk | grep -E -i 'disk|磁盘' | grep -E -i 'sd|vd' | awk '{ print $4 }' | sed 's/G//g'`
  disk_total=`cat /proc/partitions | grep -w "0" |grep -E -i 'sd|vd' | awk '{print $3}'`

  # SUSE lsblk -m | grep -E -i 'disk|磁盘' | grep -E -i 'sd|vd'  | awk 'NR==1{ print $2 }'
  net_detial=$(get_net)
  cpu_detial=$(get_cpu)
  disk_detial=$(get_disk)
  netstat_detial=$(get_netstat)
  install_date=`ls -lact --full-time /etc/ | awk 'END {print $6,$7,$8}'`
#dict
  echo "{\
    \"os_sys\":\"$os_sys\",\
    \"hostname\":\"$host_name\",
    \"os_version\":\"$os_version\",\
    \"os_kernel\":\"$os_kernel\",\
    \"cpu_num\":\"$cpu_num\",\
    \"cpu_core\":\"$cpu_core\",\
    \"mem_total\":\"$[mem_total/1024]\",\
    \"product_id\":\"$product_id\",\
    \"disk_total\":\"$[disk_total/1024/1024]\",\
    \"install_date\":\"$install_date\",\
    \"network\":$net_detial,\
    \"netstat\":$netstat_detial,\
    \"cpu_model\":$cpu_detial,\
    \"logicdisk\":$disk_detial
  }"
}

echo $(get_info)

