import os,sys,web,json
urls = (
    '/nw/status',"status",
    '/nw/poke',"ref"
   )

		

class poke:
	def GET(self):
		remoteaddr = web.ctx.env.get('REMOTE_ADDR')
		remoteurl = "http://"+remoteaddr+"/nw/status"
		return remoteurl
class status:
	def GET(self):
		f=open("status","r")
		status=f.read()
		f.close()
		return status
app = web.application(urls, globals())



if __name__=="__main__":
	if os.path.isfile("neighbours")==False:
		os.system("touch neighbours")
	app.run()
