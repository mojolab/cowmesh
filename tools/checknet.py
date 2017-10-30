import sys,os
sys.path.append("../lib")
from libcowherdhsutils import *


if __name__=="__main__":
	logging.basicConfig(filename='/opt/cowherd.log', level=logging.DEBUG,format='%(asctime)s:%(levelname)s: %(message)s')
	config=ConfigParser.ConfigParser()
	config.read("/opt/cowherd.conf")
	primary=config.get("ISP","primary")
	secondary=config.get("ISP","secondary")
	if not internet():
		logging.info("Attempting restart of primary media")
		startmedia(primary)
	else:
		logging.info("Net is active...exiting")
		sys.exit()
	time.sleep(60)
	if not internet():
		logging.info("Attempting restart of secondary media")
		startmedia(secondary)
	else:
		logging.info("Net is active...exiting")
		sys.exit()
	time.sleep(60)
	if not internet():
		logging.warning("Could not start internet")
	else:
		logging.info("Started Internet")
		
