#coding=utf-8
#! /usr/bin/env python
import MySQLdb
import time
import urllib2
import urllib
from urllib import quote
import os,sys,inspect
import smtplib
import re

def sendmail(fromwho='donotknow@soufun.com',towho='lijiajia@soufun.com',subject='no subject',msgcont='no content'):
   smtp = smtplib.SMTP()
   smtp.connect("smtp邮箱服务器", "25")
   emails=[fromwho,towho,subject,msgcont]
   msgcont='''From: %s\r\nTo: %s\r\nSubject: %s\r\n\r\n%s''' % tuple(emails)
   #smtp.sendmail('movie@soufun.com', 'lijiajia@soufun.com', 'From: movie@soufun.com\r\nTo: lijiajia@soufun.com\r\nSubject: this is a email from python demo\r\n\r\nJust for test~_~')
   smtp.sendmail(fromwho,towho,msgcont)
   smtp.quit()

   

def getCurrentTime(flag='h'):
    if(flag=='h'):
        timestr=time.strftime('%H',time.localtime(time.time()))
        print timestr
        return timestr
    elif(flag=='a'):
        timestr=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
        print timestr
        return timestr

def sendSms(tel,msgcont):
    if( msgcont != ''):
    	url = '短信接口/sendsms.do?name=test&pwd=test&dst='+tel+'&msg='+quote(msgcont)
    	result = urllib2.urlopen(url).read()
    	return result 
def script_path():
    caller_file=inspect.stack()[1][1] # caller's filename
    return os.path.abspath(os.path.dirname(caller_file))# path

def getSelfFilePath(flag='a'):
    if flag=='a':
	print script_path()
	tmptuple=[script_path(),__file__]
	tmp='%s/%s' % tuple(tmptuple)
    elif flag=='l':
	tmptuple=[script_path(),os.path.splitext(__file__)[0],'txt']
        tmp= '%s/%s.%s' % tuple(tmptuple)
    return tmp

#def wireFile(str,filename='/www/logs/resin/logs/monitorproject14News.txt'):
def wireFile(str,filename=getSelfFilePath('l')):
    fileHandle = open (filename, 'a')
    fileHandle.write ( str )
    fileHandle.close()

#def reafFile(filenames='/www/logs/resin/logs/monitorproject14News.txt'):
def reafFile(filenames=getSelfFilePath('l')):
    if os.path.exists(filenames):
    	fileHandle = open (filenames) 
    	content=fileHandle.read()
    	fileHandle.close()
    	print content
    else:
	content=""
    return content
def getCountFromStr(str):
    tmp=str.split('#')
    return tmp


def write():
    while(1):
    	try:
    		conn=MySQLdb.connect(host='mysql服务器ip',user='用户名',passwd='密码',db='数据库名',port=3331,charset="utf8")
    		cur=conn.cursor()
		sqlstr = raw_input('>>')
		#sqlstr =  ''' SELECT token FROM sendUser WHERE imei7  = '9688ec7112c61bead281b792809f1ee672d857fa' '''
		print sqlstr
    		cur.execute(sqlstr)
    		#for data in cur.fetchall():
	    	#	print  data
		print "Number of rows inserted: %d" % cur.rowcount
    		#print sqlstr
    		cur.close()
		conn.commit ()
    		conn.close()
    	except MySQLdb.Error,e:
        	print "Mysql Error %d: %s" % (e.args[0], e.args[1])


if __name__=="__main__":
    print("main")
    write()




