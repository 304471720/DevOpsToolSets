from xmlrpclib import ServerProxy
import sys
import re
import thread
import time
import threading

days=0
format='%20s|%20s|%20s|%20s|%25s|%25s|%25s'
command=""
def getData(ip,command):
	s = ServerProxy("http://"+ip+":8989")
	#if 'command' in dir() and len(command)>0:
	if command == "getApnsConsummerStatus":
		logs='%20s|%s' % (ip, s.process(command,days))
	elif command == "restartApnsConsummer":
		logs='%20s|%s' % (ip, s.process(command,days))
        elif command == "fetch_fail_token":
                logs='%s' % (s.process(command,days))
	elif 'command' in dir() and len(command)>0: 
    		logs='%20s|%s' % (ip,s.process(command,days))
	else:
        	logs= format % (ip,s.process("getSuccessCount",days),s.process("getFailedCount",days),s.process("getAllCount",days),s.process("getAverageTimeUse",days),s.process("getproject14BeginTime",days),s.process("getproject14EndTime",days))
	print logs
	#thread.exit_thread()
        return logs


class Processor(threading.Thread):
	def __init__(self, t_name , p_ip,p_command):
		threading.Thread.__init__(self,name=t_name)
		self.ip=p_ip
		self.command=p_command
	def run(self):
		getData(self.ip,self.command)
	
if __name__ == '__main__':
    servers_ip = ['serverip1','serverip2']
    if len(sys.argv)==2:
    	#command = re.findall("^\w{64}$",sys.argv[1])
    	command = sys.argv[1]
    elif len(sys.argv)==3:
	targetip=sys.argv[1]
	command = sys.argv[2]
	getData(targetip,command)
	sys.exit(1)
    else:
        header=format % ("ip","getSuccessCount","getFailedCount","getAllCount","getAverageTimeUse","getproject14BeginTime","getproject14EndTime")
        splitline = format % ("--------------------","--------------------","--------------------","--------------------","-------------------------","-------------------------","-------------------------")
        print header
        print splitline
    for ip in servers_ip:
	process_thread=Processor('test',ip,command)
	process_thread.start()
	#getData(ip,command)
	#time.sleep(1)
	#print ip,command
