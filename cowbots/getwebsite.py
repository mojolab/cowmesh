#!/usr/bin/python

from bs4 import BeautifulSoup
import urllib2,urlparse
import sys,os
sys.path.append("/opt/livingdata/lib")
from livdatcsvlib import *
baseurl="http://environicsindia.in"
webcontent=urllib2.urlopen(baseurl).read()
soup = BeautifulSoup(webcontent,'html.parser')
links=[]

for link in soup.find_all("a"):
    #print link.get('href')
    links.append(link.get('href'))



links=list(set(links))
if "#" in links:
	links.remove("#")
if None in links:
	links.remove(None)

def separateinternallinks(links):
	inlinks=[]
	outlinks=[]
	for link in links:
		if link.startswith("/")==False and link.startswith(baseurl)==False:
			#print link
			outlinks.append(link)
		else:
			inlinks.append(link)
	#print inlinks,outlinks
	return (inlinks,outlinks)
	

depth=50
d=0
seplinks=separateinternallinks(links)
inlinks=seplinks[0]
outlinks=seplinks[1]

#print inlinks #, outlinks


finalinlinks=[]
while True:
	for link in inlinks:
		if link.startswith("/"):
			link=urlparse.urljoin(baseurl,link)
		try:
			response=urllib2.urlopen(link)
			webContent=response.read()
			linksoup=BeautifulSoup(webContent,'html.parser')
			newlinks=[]
			for l in linksoup.find_all("a"):
				newlinks.append(l.get('href'))
			newlinks=list(set(newlinks))
			if "#" in newlinks:
				newlinks.remove("#")
			if None in newlinks:
				newlinks.remove(None)
			#print "New Links", newlinks
			seplinks=separateinternallinks(newlinks)
			
			finalinlinks=list(set(inlinks+seplinks[0]))
			outlinks=list(set(outlinks+seplinks[1]))
			if finalinlinks==inlinks or d==depth:
				break
			else: 
				inlinks=finalinlinks
				d+=1
				print "numlinks",len(inlinks),"depth",d
		except:
			print "Could not get page"
			continue
	if finalinlinks==inlinks or d==depth:
		break
print len(inlinks), len(outlinks)
			
inlinklist=[]
outlinklist=[]
for link in inlinks:
	dictionary={}
	if link.startswith("/"):
		linkurl=urlparse.urljoin(baseurl,link)
	dictionary['url']=linkurl
	inlinklist.append(dictionary)
inlinkssheet=CSVFile()
inlinkssheet.colnames=['url']
inlinkssheet.matrix=inlinklist


for link in outlinks:
	dictionary={}
	if link.startswith("/"):
		linkurl=urlparse.urljoin(baseurl,link)
	dictionary['url']=linkurl
	outlinklist.append(dictionary)
outlinkssheet=CSVFile()
outlinkssheet.colnames=['url']
outlinkssheet.matrix=outlinklist
c=ExcelFile()
c.worksheets.append(inlinkssheet)
c.worksheets.append(outlinkssheet)
c.worksheetnames.append("Internal LInks")
c.worksheetnames.append("External LInks")

c.exportfile("/home/arjun/ETLinks.xlsx")
