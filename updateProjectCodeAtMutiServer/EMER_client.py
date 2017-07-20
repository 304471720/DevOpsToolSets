from xmlrpclib import ServerProxy
import sys
import re
import thread
import time
import threading
from optparse import OptionParser
import subprocess
import os
serverport="5020"

def UpdateCode(ip,command):
	print "UpdateCode",ip,command
	#return ""
	out=""
	try:
        	s = ServerProxy("http://"+ip+":"+serverport)
 		out = s.process_commnand(command)
		print "_______>>>__________>>>___________>>>___________>>>__________----->> %s:" % (ip)
		print out
	except Exception,data:
                print ip,command,Exception,":",data
        return out

def UpdateCodeWithPort(ip,port,command):
        print "UpdateCodeWithPort",ip,port,command
        #return ""
	out=""
	try:
        	s = ServerProxy("http://"+ip+":"+serverport)
        	out = s.process_commnand_with_port(command,port)
        	print "=======>>>==========>>>==========>>>============>>>==========----->>%s:%s" % (ip,port)
        	print out
	except Exception,data:
		print ip,command,Exception,":",data
        return out


class Processor_By_Port(threading.Thread):
	def __init__(self, t_name , p_ip,p_port,p_command):
		threading.Thread.__init__(self,name=t_name)
		self.ip=p_ip
		self.port=p_port
		self.command=p_command
		self.remark=t_name
	def run(self):
		#print 'run thread Processor_By_Port ',self.remark
		UpdateCodeWithPort(self.ip,self.port,self.command)

class Processor(threading.Thread):
        def __init__(self, t_name , p_ip,p_command):
                threading.Thread.__init__(self,name=t_name)
                self.ip=p_ip
                self.command=p_command
		self.remark=t_name
        def run(self):
		#print 'run thread Processor ',self.remark
                UpdateCode(self.ip,self.command)


def getIp_IpPort_List(ipPorts):
	ip_list=[]
	ip_port_list=[]
	for item in ipPorts:
		isFormated=re.search('^(\d+)\.(\d+)\.(\d+)\.(\d+):(\d+,){0,}(\d+)$',item)	
		if isFormated:
			ip_ports=item.split(':')
			ip=ip_ports[0]
			ip_list.append(ip)
			ports=ip_ports[1].split(',')
			for port in ports:
				ip_port_list.append("%s:%s" % (ip,port))

	#print ip_list
	#print ip_port_list	
	return ip_list,ip_port_list
		
if __name__ == '__main__':
    soufun_servers_ip = \
       [
        'serverip1:port1,port2,port3,port4,port5,port6,port7', \
        'serverip2:port1,port2,port3,port4,port5,port6,port7'
       ]

    agent_servers_ip =  \
	[ \
        'serverip1:port1,port2,port3,port4,port5,port6,port7', \
        'serverip2:port1,port2,port3,port4,port5,port6,port7'
	]
    fang_ip_list,fang_ip_port_list = getIp_IpPort_List(soufun_servers_ip)
    agent_ip_list,agent_ip_port_list = getIp_IpPort_List(agent_servers_ip)
    #for xx in fang_ip_port_list:
#	tmp=xx.split(":")
#	print ''' INSERT INTO monitor_product_info VALUE ('fang_app','%s','%s'); ''' % (tmp[0],tmp[1])
#    sys.exit(0)
    
    parser = OptionParser(usage="usage:%prog [optinos] filepath")
    parser.add_option("-a", "--ip",  
                action = "store",  
                dest = "ip",  
                default = None,  
                help="Specify interface ip"  
                )
    parser.add_option("-p", "--port",
                action = "store",
                dest = "port",
                default = None,
                help="Specify interface port"
                )
    parser.add_option("-c", "--cmd",
                action = "store",
                dest = "command",
                default = None,
                help="Specify command "
                )

    parser.add_option("-t", "--type",
                action = "store",
                dest = "type",
                default = None,
                help="Specify product servers"
                )

    (options, args) = parser.parse_args()
    print  options.ip,options.port,options.command    
    if options.ip and options.port and options.command:
	UpdateCodeWithPort(options.ip,options.port,options.command)
    elif options.ip and options.command and not options.port:
	UpdateCode(ip,options.command)
    elif options.command and not options.ip  and not options.port:
	serverips=[]
	serveripports=[]
	if options.command.startswith("soufun_"):
		serverips= fang_ip_list
		serveripports=fang_ip_port_list
	elif options.command.startswith("agent_"):
		serverips= agent_ip_list
		serveripports=agent_ip_port_list
	elif options.type=="soufun":
                serverips= fang_ip_list
                serveripports=fang_ip_port_list
	elif options.type=="agent":
                serverips= agent_ip_list
                serveripports=agent_ip_port_list

	
	if options.command.endswith("_by_port"):
        	for ip_port in serveripports:
                	ipport=ip_port.split(':')
                	ip=ipport[0]
                	port=ipport[1]
			
			process_thread_by_port=Processor_By_Port('execute on all servers by port',ip,port,options.command)
        		process_thread_by_port.start()
			#UpdateCodeWithPort(ip,port,options.command)
	else:
		for ip in serverips:
			process_thread=Processor('execute on all servers',ip,options.command)
        		process_thread.start()
			#UpdateCode(ip,options.command)

