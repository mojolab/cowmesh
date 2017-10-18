#!/bin/bash
sudo killall hostapd
sudo service chilli stop
sudo ifdown wlan0
sudo hostapd /etc/hostapd/hostapd.conf &
sudo service chilli start
