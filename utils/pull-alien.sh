#!/bin/bash

if [ -z "$1" ]; then
    echo "specify AliEn (xrootd-xalienfs) version, for example: 1.0.14n"
    echo "http://alitorrent.cern.ch/src/xalienfs"
    exit 1
fi

wget http://alitorrent.cern.ch/src/xalienfs/xrootd-xalienfs-$1.tar.gz
