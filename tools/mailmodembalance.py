#!/usr/bin/python

import sys,os
from datetime import *

sys.path.append("/opt/mojomailman/mojomail")
from mojomail import *
if __name__=="__main__":
    mailconfig="/opt/cowmail/mail.conf"
    mailer=MojoMailer(mailconfig)
    #mailer.logintoinmail()
    messager=MojoMessager(mailconfig)
    subdict=messager.getsubdict()
    bodydict=messager.getbodydict()
    timestamp=datetime.datetime.now()
    print timestamp
    subdict['TIMESTAMP']=timestamp.strftime("%Y-%b-%d %H:%M:%S")
    subdict['MOJOMAIL']="COWHerd Report"
    subdict['TYPE']="BalanceUpdate"
    bodydict['CONTENT']=os.popen("python checkmodembal.py").read().strip()
    msg=messager.composemessage(mailer.outusername,subdict,bodydict,"")
    mailer.sendmsg(msg)
				
