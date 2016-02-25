import json,os

if __name__=="__main__":
	status={}
	status['hostname']=os.popen("hostname").read().strip()
	#status['ip']=os.popen
	iplinks=os.popen("ip link show | grep 'state UP'").read().strip().split("\n")
	status['ips']=[]
	for link in iplinks:
		iface=link.split(": ")[1]
		print iface,os.popen("ip addr show %s | grep 'inet '" %iface).read().strip().split(" ")[1].split("/")[0]
		
	f=open("status","w")
	f.write(json.dumps(status))
	f.close()
