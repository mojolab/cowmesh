import os,sys,web,json
from nwutils import *
urls = (
    '/nw/status/default',"status_default",
    '/nw/status',"status_default",
    '/nw/status/ext',"status_ext",
    '/nw/poke',"poke",
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
		statusfull=get_status_full()
		return json.dumps(statusfull)


class status_default:
	def GET(self):
		update_status(configfile)
		statusfull=get_status_full()
		status=get_status_for_default_context(configfile,statusfull)
		return json.dumps(status)
		#return json.dumps(status)
app = web.application(urls, globals())



if __name__=="__main__":
	if os.path.isfile("status")==False:
		os.system("touch status")
	app.run()
