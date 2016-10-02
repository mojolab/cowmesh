#!/bin/bash

date +%Y-%m-%d-%H:%M >> mesh.log
ping $1 -c 20 >> mesh.log &


