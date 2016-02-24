#!/usr/bin/python

import os,sys

def get_hosts(hostfile):
	hosts=[]
	f=open(hostfile,"r")
	lines=f.readlines()
	for line in lines:
		dictionary={}
		ip=line.strip().split("\t")[0].lstrip().rstrip()
		hostname=line.strip().split("\t")[1].lstrip().rstrip()
		dictionary['IP']=ip
		dictionary['HOSTNAME']=hostname
		hosts.append(dictionary)
	return hosts
if __name__=="__main__":
	srcpath=sys.argv[1]
	hosts=get_hosts(sys.argv[2])
	destpath=sys.argv[3]
	username="pi"
	outputs=[]
	for host in hosts:
		dictionary={}
		print "scp -r %s %s@%s:%s" %(srcpath,username,host['HOSTNAME'],destpath)
		try:
			output=os.popen("scp -r %s %s@%s:%s" %(srcpath,username,host['HOSTNAME'],destpath)).read().strip()
		except:
			output="Failed"

		dictionary['HOST']=host['HOSTNAME']
		dictionary['OUTPUT']=output
		outputs.append(dictionary)
	for output in outputs:
		print "*****************************************************************"
		print "Host: " + output['HOST']
		print "------------------------"
		print "Command:"
		print "------------------------"
		print output['OUTPUT']
		print "*****************************************************************"

