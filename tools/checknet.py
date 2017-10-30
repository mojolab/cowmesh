import sys,os
sys.path.append("../lib")
from libcowherdutils import *


if __name__=="__main__":
    config=ConfigParser.ConfigParser()
    config.read("/opt/cowherd.conf")
    primary=config.get("ISP","primary")
    secondary=config.get("ISP","secondary")
    if not internet():
        startmedia(primary)
    time.sleep(60)
    if not internet():
        startmedia(secondary)

