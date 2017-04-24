from bs4 import BeautifulSoup
import urllib2,urlparse
import sys,os
sys.path.append("/opt/livingdata/lib")
from livdatcsvlib import *
def gettextandlinks(url):
    webcontent=urllib2.urlopen(url).read()
    soup = BeautifulSoup(webcontent,'html.parser')
    links=[]
    text=""
    for p in soup.find_all("p"):
        text=text+"\n"+ p.getText()
    for link in soup.find_all("a"):
        links.append(link.get('href'))
    return (text,links)