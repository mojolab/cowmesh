#!/usr/bin/python

import socket
import time,os,sys,ConfigParser
import logging


def internet(host="8.8.8.8", port=53, timeout=3):
    """
    Host: 8.8.8.8 (google-public-dns-a.google.com)
    OpenPort: 53/tcp
    Service: domain (DNS/TCP)                                 
    """
    logging.info("Checking if Internet is active")
    try:
        socket.setdefaulttimeout(timeout)
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
        return True
    except Exception as ex:
        logging.info(ex)
        return False


def startmedia(media):
    if "eth" in media:
        os.system("sudo sh /opt/cowmesh/tools/starteth.sh")
    if "ppp" in media:
        os.system("sudo sh /opt/cowmesh/tools/startmodem.sh")
