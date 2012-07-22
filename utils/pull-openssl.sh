#!/bin/bash

if [ -z "$1" ]; then
    echo "specify OpenSSL version, for example: 0.9.8x"
    echo "http://www.openssl.org/source"
    exit 1
fi

wget http://www.openssl.org/source/openssl-$1.tar.gz
