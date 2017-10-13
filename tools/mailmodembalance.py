#!/usr/bin/python

import sys

sys.path.append("/opt/mojomailman/mojomail")
from mojomail import *
if __name__=="__main__":
    mailconfig="/opt/mail.conf"
    mailer=MojoMailer(mailconfig)
    mailer.logintoinmail()
    messager=MojoMessager(mailconfig)
    bodydict['
