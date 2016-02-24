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
	hosts=get_hosts(sys.argv[1])
	command=sys.argv[2]
	username="pi"
	outputs=[]
	for host in hosts:
		dictionary={}
		try:
			output=os.popen("ssh %s@%s '%s'" %(username,host['HOSTNAME'],command)).read().strip()
		except:
			output="Failed"

		dictionary['HOST']=host['HOSTNAME']
		dictionary['COMMAND']=command
		dictionary['OUTPUT']=output
		outputs.append(dictionary)
	for output in outputs:
		print "*****************************************************************"
		print "Host: " + output['HOST']
		print "------------------------"
		print "Command:"
		print "------------------------"
		print output['COMMAND']
		print "Output:"
		print "------------------------"
		print output['OUTPUT']
		print "*****************************************************************"

