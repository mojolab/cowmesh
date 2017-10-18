#!/bin/bash
sudo ip route del default
sudo ifdown eth0
sudo ifup eth0
sudo echo "nameserver 4.2.2.2" > /etc/resolv.conf
sudo sh /opt/cowmesh/tools/ishare.sh eth0
