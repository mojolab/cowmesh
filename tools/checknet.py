#!/usr/bin/python
import socket
import time,os,sys,ConfigParser
def internet(host="8.8.8.8", port=53, timeout=3):
    """
    Host: 8.8.8.8 (google-public-dns-a.google.com)
    OpenPort: 53/tcp
    Service: domain (DNS/TCP)                                 
    """
    try:
        socket.setdefaulttimeout(timeout)
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
        return True
    except Exception as ex:
        print ex
        return False


def startmedia(media):
    if "eth" in media:
        os.system("sudo sh /opt/cowmesh/tools/starteth.sh")
    if "ppp" in media:
        os.system("sudo sh /opt/cowmesh/tools/startmodem.sh")


if __name__=="__main__":
    config=ConfigParser.ConfigParser()
    config.read("/opt/cowherd.conf")
    primary=config.get("ISP","primary")
    secondary=config.get("ISP","secondary")
    if not internet():
        startmedia(primary)
    time.sleep(10)
    if not internet():
        startmedia(secondary)

