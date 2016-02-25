import os,sys,web,json
from nwutils import *
urls = (
    '/nw/status/base',"status_base",
    '/nw/status',"status_base",
    '/nw/status/ext',"status_ext",
    '/nw/poke',"ref",
    '/nw/rqi',"requester_info"
   )

configfile="./nwconfig.conf"


class requester_info:
	def GET(self):
		requesterinfo={}
		keys=web.ctx.env.keys()
		for key in keys:
			requesterinfo[key]=str(web.ctx.env.get(key))
		#return requesterinfo
		
		return json.dumps(requesterinfo)


class poke:
	def GET(self):
		remoteaddr = web.ctx.env.get('REMOTE_ADDR')
		remoteurl = "http://"+remoteaddr+"/nw/status"
		return remoteurl

class status_ext:
	def GET(self):
		update_status(configfile)
		f=open("status","r")
		statusfull=json.load(f)
		f.close()
		#return statusfull
		return json.dumps(statusfull)


class status_base:
	def GET(self):
		update_status(configfile)
		f=open("status","r")
		statusfull=json.load(f)
		f.close()
		status={}
		status['hostname']=statusfull['hostname']
		
		return json.dumps(status)
		#return json.dumps(status)
app = web.application(urls, globals())



if __name__=="__main__":
	if os.path.isfile("status")==False:
		os.system("touch status")
	app.run()
