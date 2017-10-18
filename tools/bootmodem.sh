#!/bin/bash
sudo sh /opt/cowmesh/tools/shutdownhs.sh
sleep 5
sudo sh /opt/cowmesh/tools/startmodem.sh
sleep 5
sudo sh /opt/cowmesh/tools/setuphotspot.sh

