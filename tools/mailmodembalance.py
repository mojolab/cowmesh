#!/usr/bin/python

import sys,os
from datetime import *
sys.path.append("../lib")
from libcowherdhsutils import *

sys.path.append("/opt/mojomailman/mojomail")
from mojomail import *
if __name__=="__main__":
	logging.basicConfig(filename='/opt/cowherd.log', level=logging.DEBUG,format='%(asctime)s:%(levelname)s: %(message)s')
	mailconfig="/opt/cowconf/mail.conf"
	mailer=MojoMailer(mailconfig)
	#mailer.logintoinmail()
	messager=MojoMessager(mailconfig)
	subdict=messager.getsubdict()
	bodydict=messager.getbodydict()
	timestamp=datetime.datetime.now()
	subdict['TIMESTAMP']=timestamp.strftime("%Y-%b-%d %H:%M:%S")
	subdict['MOJOMAIL']=mailer.name
	subdict['TYPE']="BalanceUpdate"
	logging.info("Getting balance update from modem")
	balenq=os.popen("python checkmodembal.py").read().strip()
	bodydict['CONTENT']=balenq
	logging.info(balenq)
	msg=messager.composemessage(mailer.outusername,subdict,bodydict,"")
	mailer.sendmsg(msg)
	logging.info("Sent balance update")
				
