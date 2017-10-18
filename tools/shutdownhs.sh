#!/bin/bash
sudo service chilli stop
sudo killall wvdial
sudo killall hostapd
sudo ifdown wlan0
