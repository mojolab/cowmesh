#!/usr/bin/python
import os,sys

automountdir="/media"

if __name__=="__main__":
	mediadirs=os.listdir(automountdir)
	dirstoclean=[]
	for directory in mediadirs:
		mountpath=os.path.join(automountdir,directory)
		devtoclean=os.popen("sudo mount | grep '%s'" %mountpath).read().strip().split(" ")[0]
		print mountpath,devtoclean
		if devtoclean != "":
			os.system("sudo umount %s" %mountpath)
		if os.path.isdir(mountpath):
			os.rmdir(mountpath)
		



#sudo umount /media/arjun
#sudo mount /dev/sda1 /media/arjun -o uid=www-data,gid=www-data 
