#!/bin/bash
sudo ip route del default
sudo killall wvdial
sleep 10
sudo wvdial &
sleep 10
sudo sh /opt/cowmesh/tools/ishare.sh ppp0
