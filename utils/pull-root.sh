#!/bin/bash

if [ -z "$1" ]; then
    echo "specify ROOT SVN version tag (without v), for example: 5-33-02b"
    echo "list of all tags: svn list https://root.cern.ch/svn/root/tags"
    exit 1
fi

SVN_PATH1="root_svn$1"
SVN_PATH2="root_v$1"

svn co https://root.cern.ch/svn/root/tags/v$1 $SVN_PATH1
svn -q export $SVN_PATH1 $SVN_PATH2
tar cfz $SVN_PATH2.tar.gz $SVN_PATH2
rm -rf $SVN_PATH1
