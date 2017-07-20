from SimpleXMLRPCServer import (SimpleXMLRPCServer,SimpleXMLRPCRequestHandler)
import SocketServer
import commands
import sys
import re
import socket
import time
import subprocess
import signals
from urllib import quote
import urllib2
import urllib
import datetime


import smtplib
from email.MIMEBase import MIMEBase
from email.MIMEText import MIMEText
from email.MIMEMultipart import MIMEMultipart
import email

SimpleXMLRPCServer.allow_reuse_address = 1


class MyEmail:
  """this moudle is for send email ljj 2015.08.06"""
  def __init__(self,femail='mobile@staff.xxxx.com',fpwd='password',tmail='lijiajia@xxxx.com',subject='hello',mybody='this letter is from xxxx.com'):
      self.femail=femail
      self.fpwd=fpwd
      self.temail=tmail
      self.mybody=mybody
      self.subject=subject
  def SendEmail(self):     
      my_body=self.mybody     
      msg=MIMEMultipart()
      msg['From'] = self.femail
      msg['To'] = self.temail
      msg['Subject'] =  self.subject
      msg['Reply-To'] = self.femail
      msg['Date'] = time.ctime(time.time())
      msg['X-Priority'] =  '''3'''
      msg['X-MSMail-Priority'] =  '''Normal'''      
      body=email.MIMEText.MIMEText(self.mybody,_subtype='html',_charset='gb2312')
      msg.attach(body)
      s = smtplib.SMTP('smtp.staff.xxxx.com')
      s.esmtp_features["auth"]="LOGIN PLAIN"
      s.starttls()
      s.login(self.femail,self.fpwd)
      s.sendmail(self.femail,self.temail,msg.as_string())
      s.close()

def getLocalIp():
	command='''cat /etc/sysconfig/network-scripts/ifcfg-eth1 | grep IPADDR | awk -F '=' '{printf $2}' '''
	result=getShellExecuteResult(command)
        return  "".join(result)

def reset_sigpipe():
    signal.signal(signal.SIGPIPE, signal.SIG_DFL)

def getShellExecuteResult(shell_commands):
	output = subprocess.Popen(shell_commands, shell=True, preexec_fn=reset_sigpipe, stdout=subprocess.PIPE)
	return output.stdout.readlines()

def GetNowTime():
    return time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(time.time()))


visitor={'vistorip':'xxx.xxx.xx.xx','startuptime':GetNowTime(),'lastvisittime':'','localip':getLocalIp(),'maillist':'lijiajia@xxxx.com'}
def sendSms(tel,msgcont):
    if( msgcont != ''):
        url = 'http://短信API?name=test&pwd=test&dst='+tel+'&msg='+quote(msgcont)
        result = urllib2.urlopen(url).read()
        return result
def wireFile(str,filename='/www/logs/resin/logs/EMER_server.txt'):
    fileHandle = open (filename, 'a')
    fileHandle.write ( str )
    fileHandle.close()

def reafFile(filenames='/www/logs/resin/logs/EMER_server.txt'):
    if os.path.exists(filenames):
        fileHandle = open (filenames)
        content=fileHandle.read()
        fileHandle.close()
        #print content
    else:
        content=""
    return content

def process_commnand(commandname,param):
	print commandname
	print param
	if commandname=="xxxx_upgrade":
		command=" cd /www/3g.client.xxxx.com/project4 \r\n"
		if param and len(param.split(";")) > 0:
                	for s in param.split(";"):
				s=s.strip('\n')
                        	str=''' sudo svn up  %s \r\n''' % (s)
				if s!="":
					command = command + str
			command = command + " ant build "
		print command
	elif commandname=="xxxx_version":
                command=" cd /www/3g.client.xxxx.com/project4 \r\n"
                if param and len(param.split(";")) > 0:
                        for s in param.split(";"):
                                s=s.strip('\n')
                                str=''' sudo svn st -v  %s \r\n''' % (s)
                                if s!="":
                                        command = command + str
                print command
        elif commandname=="agent_upgrade":
                command=''' 
                        cd /www/3g.client.xxxx.com/productA
                        svn st -v src/readdb.properties 
                        ant build
                        '''
	elif commandname=="suicide":
		command=" kill -9  `ps aux | grep %s | grep -v grep | grep -v nohup | awk '{print $2}'` " % (__file__)
	else:
		command="invalid command!!!"
	cmd_result=getShellExecuteResult(command)
 	return  "".join(command)+"\r"+"".join(cmd_result)

def process_diy_command(command,dir,param):
	
	cmd_result=getShellExecuteResult(command)
        print  "".join(command)+"\r"+"".join(cmd_result)
        return  "".join(command)+"\r"+"".join(cmd_result)


def process_commnand_with_port(commandname,port):
        print commandname
	print port
        if commandname=="xxxx_checkstatus_by_port":
                command=''' sudo sh /etc/init.d/xxxxapp.xxxx.com-%s.sh status ''' % (port)
        elif commandname=="xxxx_checklogs_by_port":
                command=''' cat /logs/resin/logs/jvm-xxxx-%s.log |tail -n20 ''' % (port)
        elif commandname=="xxxx_restart_server_by_port":
                command=''' 
			sudo sh /etc/init.d/xxxxapp.xxxx.com-%s.sh stop
			sudo sh /etc/init.d/xxxxapp.xxxx.com-%s.sh start
			''' % (port,port)
        elif commandname=="agent_checkstatus_by_port":
                command=''' sudo sh /etc/init.d/productB.3g.xxxx.com_%s_resin4.sh   status  '''
        elif commandname=="agent_restart_server_by_port":
                command=''' 
			sudo sh /etc/init.d/productB.3g.xxxx.com_%s_resin4.sh stop
			sudo sh /etc/init.d/productB.3g.xxxx.com_%s_resin4.sh start
		        ''' % (port,port)
        else:
                command="invalid command!!!"
        cmd_result=getShellExecuteResult(command)
        return  "".join(command)+"\r"+"".join(cmd_result)

class MyRequestHandler(SimpleXMLRPCRequestHandler):
    def __init__(self, request, client_address, server):
	self.ip,self.port=client_address
	global visitor
	if self.ip != visitor['vistorip']:
		log= " localip:%s . invalid address %s:%d " % (visitor['localip'],self.ip,self.port)
                send=MyEmail('mobile@staff.xxxx.com','password',visitor['maillist'],'operate server batch',log)
                send.SendEmail()
		return
	else:
		if visitor['lastvisittime'] == '':
			visitor['lastvisittime']=GetNowTime()
		else:
			lastvisittime=visitor['lastvisittime']
			lasttime=time.strptime(lastvisittime,'%Y-%m-%d %H:%M:%S')
			currtime=time.strptime(GetNowTime(),'%Y-%m-%d %H:%M:%S')
			lasttimedate=datetime.datetime(lasttime[0],lasttime[1],lasttime[2],lasttime[3],lasttime[4],lasttime[5])
			currtimedate=datetime.datetime(currtime[0],currtime[1],currtime[2],currtime[3],currtime[4],currtime[5])
			interval= currtimedate-lasttimedate
			#if interval.seconds < 2:
			#	log= "localip:%s .last visit time %s, too many connection from: %s:%d " % (visitor['localip'],visitor['lastvisittime'],self.ip,self.port)
			#	print log
			#	send=MyEmail('mobile@staff.xxxx.com','password',visitor['maillist'],'operate server batch',log)
			#	send.SendEmail()
			#	return
		print  visitor
		visitor['lastvisittime']=GetNowTime()
		log= "localip %s ,visit time :%s  from  %s:%d " % (visitor['localip'],visitor['lastvisittime'],self.ip,self.port)
		print log
		send=MyEmail('mobile@staff.xxxx.com','password',visitor['maillist'],'operate server batch',log)
                send.SendEmail()
        	SimpleXMLRPCRequestHandler.__init__(self, request, client_address, server)

class RPCThreading(SocketServer.ThreadingMixIn, SimpleXMLRPCServer):
    pass

if __name__ == '__main__':
    #s = SimpleXMLRPCServer((visitor['localip'], 5020),requestHandler=MyRequestHandler)
    s = RPCThreading((visitor['localip'],5020),requestHandler=MyRequestHandler)
    s.register_function(process_commnand)
    #s.register_function(process_diy_command)
    s.register_function(process_commnand_with_port)
    s.serve_forever()
