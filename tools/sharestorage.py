#!/usr/bin/python
import os,sys,copy

automountdir="/media"

if __name__=="__main__":
	mediadirs=os.listdir(automountdir)
	excludedirs=["csv","cowmesh"]
	dirstoshare=copy.copy(mediadirs)
	
	for direc in excludedirs:
		if direc in mediadirs:
			dirstoshare.remove(direc)
	for dirtoshare in dirstoshare:
		dirtoshare=os.path.join(automountdir,dirtoshare)
		devtoshare=os.popen("sudo mount | grep '%s'" %dirtoshare).read().strip().split(" ")[0]
		print dirtoshare,devtoshare 
		os.system("sudo umount %s" %dirtoshare)
		if os.path.isdir(dirtoshare)==False:
			os.mkdir(dirtoshare)
		os.system("sudo mount %s %s -o uid=www-data,gid=www-data" %(devtoshare,dirtoshare)) 



#sudo umount /media/arjun
#sudo mount /dev/sda1 /media/arjun -o uid=www-data,gid=www-data 
