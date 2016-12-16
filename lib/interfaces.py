import os
hw_protocols=['ip']


def get_ipifaces():
	iplinks=os.popen("ip link show | grep 'state UP'").read().strip().split("\n")
	ips=[]
	for link in iplinks:
		dictionary={}
		iface=link.split(": ")[1]
		ipaddr=os.popen("ip addr show %s | grep 'inet '" %iface).read().strip().split(" ")[1].split("/")[0]
		#print iface,ipaddr
		dictionary['name']=iface
		dictionary['addr']=ipaddr
		dictionary['protocol']="ip"
		ips.append(dictionary)
	return ips

def get_ifaces_for_protocol(protocol):
	if protocol=="ip":
		ifaces=get_ipifaces()
	return ifaces

def get_hw_interfaces():
	hw_interfaces=[]
	for protocol in hw_protocols:
		ifaces=get_ifaces_for_protocol(protocol)
		hw_interfaces=hw_interfaces+ifaces
	return hw_interfaces
