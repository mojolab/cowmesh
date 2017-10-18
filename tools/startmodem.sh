#!/bin/bash
sudo ip route del default
sudo killall wvdial
sleep 20
sudo wvdial &
sleep 30
sudo sh /opt/cowmesh/tools/ishare.sh ppp0
sudo echo "nameserver 4.2.2.2" > /etc/resolv.conf
