#！/bin/sh
logfilename=""
logpath=""
IP=""
createfile()
{
    #logpath="/home/wireless_group2/log/"
    currenttime=`date "+%Y%m%d"`
    logfilename=${logpath}SERVERMONITOR_${currenttime}.log
    if [ ! -d $logpath ];then
	if [ $logpath =~ "~" ];then
		echo "$logpath invalid !!! "
		exit
	fi
	ret=`mkdir -p $logpath && echo "success" || echo "fail"`
	if [ "$ret"x == "fail"x ];then
		echo "create dir fails!!!"
		exit
	fi
    fi
    if [ ! -f "$logfilename" ];then
        echo "log file $logfilename no exist !!!"
        ret1=`echo " " >> $logfilename && echo "success" || echo "fail"`
        if [ "$ret1"x == "fail"x ];then
        	echo "append string fails to $logfilename"
                exit
	else
		echo "create logfile success !!! filename : $logfilename"
        fi
    fi
}
write_log ()
{
              #createfile
              level=$1
              msg=$2
              case $level in
               debug)
               echo "[DEBUG] `date "+%Y-%m-%d %H:%M:%S"` : $msg  " >> $logfilename
               ;;
               info)
               echo "[INFO] `date "+%Y-%m-%d %H:%M:%S"` : $msg  " >> $logfilename
               ;;
               error)
               echo "[ERROE] `date "+%Y-%m-%d %H:%M:%S"` : $msg  " >> $logfilename
               ;;
               *)
               echo "error......" >> $logfilename
               ;;
               esac
}

checkpid() { #0表示失败，1表示成功
pidfile=$1
if [ ! -f "$pidfile" ]; then
	return 0
fi
pid=`cat "$pidfile"`
if [ "$pid"x != ""x ]; then
{
	ret=`ps --no-heading $pid | wc -l`
        return $ret
}
else
        return 0
fi
return 0
}

sendmsg()
{
	tel=$1
	msgcont=$(eval echo [`date "+%Y-%m-%d %H:%M:%S"`] $2 | iconv -f gb2312 -t utf8)
	r=`curl  -s "http://wireless.soufun.com/sms_validate/sendsms.do?name=test&pwd=test&&dst=$tel" -d "&msg=$msgcont" | awk '{printf $1}'`
	if [ "$r"x == "0000"x ]; then
		write_log "info" "发送报警短信成功 : $msgcont"
	else
		write_log "error" "发送报警短信 : $msgcont 失败,返回错误码$r"
	fi
	#echo  $tel $msgcont
}

pidvalue=""
telvalue=""
msgcontvalue=""
scriptvalue=""
ipvalue=""
getconfig()
{
  SECTION=$1
  CONFILE=$2
  ENDPRINT="pid tel ip msgcont script"
  echo "$ENDPRINT"
  for loop in `echo $ENDPRINT`
  do
       #这里面的的SECTION的变量需要先用双引号，再用单引号，我想可以这样理解，
       #单引号标示是awk里面的常量，因为$为正则表达式的特殊字符，双引号，标示取变量的值
       #{gsub(/[[:blank:]]*/,"",$2)去除值两边的空格内容
       #awk -F '=' '/\['"$SECTION"'\]/{a=1}a==1&&$1~/'"$loop"'/{gsub(/[[:blank:]]*/,"",$2);printf("%s\t",$2) ;exit}' $CONFILE
       value=`awk -F '=' '/\['"$SECTION"'\]/{a=1}a==1&&$1~/'"$loop"'/{print  $2;exit}' $CONFILE`
       if [ "$loop" == "pid" ];then
	     pidvalue=$value
       elif [ "$loop" == "tel" ];then
	     telvalue=$value
       elif [ "$loop" == "msgcont" ];then
	     msgcontvalue=$value
       elif [ "$loop" == "script" ];then
             scriptvalue=$value
       elif [ "$loop" == "ip" ];then
             ipvalue=$value
	     echo $ipvalue | perl -ne 'exit 1 unless /\b(?:(?:(?:[01]?\d{1,2}|2[0-4]\d|25[0-5])\.){3}(?:[01]?\d{1,2}|2[0-4]\d|25[0-5]))\b/'
	     if [ $? -eq 1 ];then
	        getOutNetIp
	     fi
       fi
       write_log "debug" "section:$SECTION config:$loop=$value"
  done
}

getOutNetIp()
{
	ipvalue=`/sbin/ifconfig | awk '{if ( $1 == "inet" && $3 ~ /^Bcast/) print $2}' | cut -f2 -d ":" | awk 'NR==2' `
	echo $ipvalue
}

#getOutNetIp
#exit

#更改变量名称
file=$0
filename=${file%.*}
filepath=`dirname $0`"/"
#configfile=${filepath}${filename}.ini
configfile=${filename}.ini
executpath=${PWD}
echo $executpath
echo $filepath
if [ $# -gt 1 ];then
	#file=$0
	#echo ${filename##*.}
	filename=${filename%.*}
	#"[usage: ] please input 2 params at least !
	#1: config filename
	#2: log filename"
	echo "params count too long!!!"
	exit
elif [ $# -eq 1 ];then
	logpath=$1
fi

if [[ $logpath =~ "/" ]];then
	echo "$logpath is a dirpath !!!"
	if [[ $logpath =~ ".*/$" ]];then
		echo "$logpath  has / suffix "
	else
		logpath=$logpath"/"
	fi
else
	logpath=${executpath}$1"/"
fi

if [ ! -f $configfile ];then
	echo "please make the ini file $configfile in the same path of the shell script"
	exit
fi
#if [ ! -d "$logpath" ];then
#	logpath=${executpath}$1
#	if [ ! -d "$logpath" ];then
#		echo "logpath $logpath is not valid!!!"
#		exit
#	else
#		echo ""
#	fi
#fi

createfile
CONFIGFILE=$configfile
#文件名称
write_log "debug"  "===========ConfigName:$CONFIGFILE==============================="
#取得ids中的每个id把，号分隔改成空格，因为循环内容要以空格分隔开来
profile=`sed -n '/SERVERNAMES/'p $CONFIGFILE | awk -F= '{print $2}' | sed 's/,/ /g'`
#对于一个配置文件中的所有id循环
for OneCom in $profile
do
  write_log "debug"  "server $OneCom"
  #此处函数调用有时候不能用反引号，不然会出错，此处原由还不清楚知道的麻烦请告之
  getconfig  $OneCom  $CONFIGFILE
  checkpid $pidvalue
  ret=$?
  if [ "$ret" -eq 0 ];then
  	sendmsg "$telvalue" "$msgcontvalue"
		#启动处理脚本
	ret=$(eval `echo $scriptvalue`)
        if [[ $? -eq 0 ]];then
		sendmsg  "$telvalue" "服务器${ipvalue},服务${SECTION}的重启脚本${scriptvalue} 执行成功!!!"
	else
		sendmsg  "$telvalue" "ERROR!!!服务器${ipvalue},服务${SECTION}的重启脚本${scriptvalue} 执行失败"
	fi
  fi
done
write_log "debug"  "========================================================"
