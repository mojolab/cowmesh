#!/usr/bin/python

import sys,os
from datetime import *
sys.path.append("../lib")
from libcowherdutil import *

sys.path.append("/opt/mojomailman/mojomail")
from mojomail import *
if __name__=="__main__":
    mailconfig="/opt/cowconf/mail.conf"
    mailer=MojoMailer(mailconfig)
    #mailer.logintoinmail()
    messager=MojoMessager(mailconfig)
    subdict=messager.getsubdict()
    bodydict=messager.getbodydict()
    timestamp=datetime.datetime.now()
    print timestamp
    subdict['TIMESTAMP']=timestamp.strftime("%Y-%b-%d %H:%M:%S")
    subdict['MOJOMAIL']=mailer.name
    subdict['TYPE']="BalanceUpdate"
    bodydict['CONTENT']=os.popen("python checkmodembal.py").read().strip()
    msg=messager.composemessage(mailer.outusername,subdict,bodydict,"")
    mailer.sendmsg(msg)
				
