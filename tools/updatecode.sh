#!/bin/bash
cd /opt/cowmesh/nw/
cp /opt/cowmesh/nw/nwconfig.conf ~/nwconfig.bck
cp /opt/cowmesh/nw/status ~/status.bck
rm /opt/cowmesh/nw/nwconfig.conf
rm /opt/cowmesh/nw/status
cd /opt/cowmesh
git pull

cp  ~/nwconfig.bck /opt/cowmesh/nw/nwconfig.conf
cp  ~/status.bck /opt/cowmesh/nw/status

