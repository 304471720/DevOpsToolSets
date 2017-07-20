from SimpleXMLRPCServer import SimpleXMLRPCServer   
import commands
import sys
import re
import socket
import time
import subprocess
import signal

def reset_sigpipe():
    signal.signal(signal.SIGPIPE, signal.SIG_DFL)

def getShellExecuteResult(shell_commands):
	output = subprocess.Popen(shell_commands, shell=True, preexec_fn=reset_sigpipe, stdout=subprocess.PIPE)
	return output.stdout.read()

def GetNowTime():
    return time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(time.time()))

def process(commandname,days=0):
	if len(re.findall("^\d$","%d" % (days)))==0:
		days=0
	if commandname=="getServerIp":
		command='''cat /etc/sysconfig/network-scripts/ifcfg-eth1 | grep IPADDR | awk -F '=' '{printf $2}' '''
        elif commandname=="fetch_fail_token":
                command=''' 
                        cat /logs/apns_amq_logs/service.log*  | grep 'send failed:token=' | grep `date "+%%Y-%%m-%%d" -d "-%dday"` | awk '{print $9}' | cut -d = -f 2 | cut -d '|' -f 1 | awk '{print $1}'
                        ''' %  (days)
	elif commandname=="getApnsConsummerStatus":
		command='''sudo sh /logs/3g.client.soufun.com/apns_amq_consumernew/apns_amq_consumernew.sh status '''
	elif commandname=="restartApnsConsummer":
		command=''' sudo sh /logs/3g.client.soufun.com/apns_amq_consumernew/apns_amq_consumernew.sh  restart '''
	elif  commandname=="getSuccessCount":
		command='''cat /logs/apns_amq_logs/service.log* |grep `date "+%%Y-%%m-%%d" -d "-%dday"` | grep 'sent successfully' | wc -l''' % (days)
	elif commandname=="getFailedCount":
		command='''cat /logs/apns_amq_logs/service.log* |grep `date "+%%Y-%%m-%%d" -d "-%dday"` | grep 'send failed:token=' | wc -l''' % (days)
	elif commandname=="getAllCount":
		command='''cat /logs/apns_amq_logs/service.log* |grep `date "+%%Y-%%m-%%d" -d "-%dday"` | grep  -P '(send failed)|(sent successfully)' | wc -l''' % (days)
	elif commandname=='''getAverageTimeUse''':
		command='''cat /logs/apns_amq_logs/service.log* |grep `date "+%%Y-%%m-%%d" -d "-%dday"` | grep 'time use :' | awk -F':| ' 'BEGIN{maxtime=0;}{sumtime+=$15;if(maxtime< $15){maxtime=$15}}END{print "avg:"(sumtime/NR)"s,max:"maxtime"s" }' ''' % (days)
	elif commandname=="getproject14BeginTime":
		command='''cat /logs/apns_amq_logs/service.log* |grep `date "+%%Y-%%m-%%d" -d "-%dday"` | grep ' sen'| sort -n | head -n 1 | awk '{printf $1" "$2}' ''' % (days)
	elif commandname=="getproject14EndTime":
		command='''cat /logs/apns_amq_logs/service.log* |grep `date "+%%Y-%%m-%%d" -d "-%dday"` | grep ' sen'| sort -n | tail -n 1 | awk '{printf $1" "$2}' ''' % (days)
	elif len(re.findall("^\w{64}$",commandname))>0:
                token=re.findall("^\w{64}$",commandname)[0]
                command='''cat /logs/apns_amq_logs/service.log* |grep `date "+%%Y-%%m-%%d" -d "-%dday"` | grep '%s' | wc -l ''' %  (days,token)
	else: 
		command="invalid command!!!"
	print command
	print commandname
	cmd_result=getShellExecuteResult(command)
	#print cmd_result
        if len(cmd_result.strip()) ==0:
        	return "Null"
        else:
        	return cmd_result.rstrip()


if __name__ == '__main__':
    s = SimpleXMLRPCServer(('0.0.0.0', 8989))
    s.register_function(process)
    s.serve_forever()
    #print process("getproject14BeginTime",20)
