#!/usr/bin/python
import os,sys,copy

automountdir="/media"

if __name__=="__main__":
	mediadirs=os.listdir(automountdir)
	excludedirs=["csv","cowmesh"]
	dirstoclean=copy.copy(mediadirs)
	
	for direc in excludedirs:
		if direc in mediadirs:
			dirstoclean.remove(direc)
			
	for directory in dirstoclean:
		mountpath=os.path.join(automountdir,directory)
		devtoclean=os.popen("sudo mount | grep '%s'" %mountpath).read().strip().split(" ")[0]
		print mountpath,devtoclean
		if devtoclean != "":
			os.system("sudo umount %s" %mountpath)
		if os.path.isdir(mountpath):
			os.rmdir(mountpath)
		



#sudo umount /media/arjun
#sudo mount /dev/sda1 /media/arjun -o uid=www-data,gid=www-data 
