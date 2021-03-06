#!/bin/bash

if [ -z "$1" ]; then
    echo "specify AliRoot SVN version tag (without v), for example: 5-04-25"
    echo "list of all tags: svn list https://alisoft.cern.ch/AliRoot/tags"
    exit 1
fi

MY_VER=${1//-/.}

SVN_PATH1="AliRoot_svn$1"
SVN_PATH2="alice-aliroot-an-$MY_VER"
WC_FILE="wc.db"

#svn co https://alisoft.cern.ch/AliRoot/tags/v$1-AN $SVN_PATH1
svn co http://svn.cern.ch/guest/AliRoot/tags/v$1-AN $SVN_PATH1
cp $SVN_PATH1/.svn/$WC_FILE $WC_FILE
svn -q export $SVN_PATH1 $SVN_PATH2
mkdir $SVN_PATH2/.svn/
mv $WC_FILE $SVN_PATH2/.svn/
tar cfz $SVN_PATH2.tar.gz $SVN_PATH2
rm -rf $SVN_PATH1
