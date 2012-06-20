#!/bin/bash

if [ -z "$1" ]; then
    echo "specify XRootD version, for example: 3.0.5"
    echo "http://www.xrootd.org/dload.html"
    exit 1
fi

wget http://www.xrootd.org/download/v$1/xrootd-$1.tar.gz
