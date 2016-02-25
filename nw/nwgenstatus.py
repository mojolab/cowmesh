import json,os

if __name__=="__main__":
	status={}
	status['hostname']=os.popen("hostname").read().strip()
	#status['ip']=os.popen
	iplinks=os.popen("ip link show | grep 'state UP'").read().strip().split("\n")
	status['ips']=[]
	for link in iplinks:
		dictionary={}
		iface=link.split(": ")[1]
		ipaddr=os.popen("ip addr show %s | grep 'inet '" %iface).read().strip().split(" ")[1].split("/")[0]
		print iface,ipaddr
		dictionary['iface']=iface
		dictionary['ipaddr']=ipaddr
		status['ips'].append(dictionary)
	f=open("status","w")
	f.write(json.dumps(status))
	f.close()
