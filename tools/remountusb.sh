#!/bin/bash
sudo umount /media/arjun
sudo mount /dev/sda1 /media/arjun -o uid=www-data,gid=www-data 
