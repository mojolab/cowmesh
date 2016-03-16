#!/usr/bin/python
import os,sys

automountdir="/media"

if __name__=="__main__":
	mediadirs=os.listdir(automountdir)
	dirstoshare=mediadirs
	for directory in dirstoshare:
		dirtoshare=os.path.join(automountdir,directory)
		devtoshare=os.popen("sudo mount | grep '%s'" %dirtoshare).read().strip().split(" ")[0]
		print dirtoshare,devtoshare 
		os.system("sudo umount %s" %dirtoshare)
		if os.path.isdir(dirtoshare)==False:
			os.mkdir(dirtoshare)
		os.system("sudo mount %s %s -o uid=www-data,gid=www-data" %(devtoshare,dirtoshare)) 



#sudo umount /media/arjun
#sudo mount /dev/sda1 /media/arjun -o uid=www-data,gid=www-data 
