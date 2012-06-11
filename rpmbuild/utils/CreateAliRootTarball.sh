#!/bin/bash

if [ -z "$1" ];then
  echo "specify tag (without v ) : 5-03-29-AN"
  exit 1
fi

MY_TAG="alice-aliroot-an-${1//-/.}"
MY_TAG=${MY_TAG/.AN/}

echo "$MY_TAG"
svn co https://alisoft.cern.ch/AliRoot/tags/v$1 $MY_TAG
tar cfz $MY_TAG.tar.gz $MY_TAG
