#!/bin/bash

if [ -z "$1" ]; then
    echo "specify GEANT3 SVN version tag (without v), for example: 1-14"
    echo "list of all tags: svn list https://root.cern.ch/svn/geant3/tags"
    exit 1
fi

G3_REV="8"
G3_VER=${1//-/.}.$G3_REV

SVN_PATH1="geant3_svn_$G3_VER"
SVN_PATH2="alice-geant3-$G3_VER"

svn co https://root.cern.ch/svn/geant3/tags/v$1 $SVN_PATH1
svn -q export $SVN_PATH1 $SVN_PATH2
tar cfz $SVN_PATH2.tar.gz $SVN_PATH2
rm -rf $SVN_PATH1
