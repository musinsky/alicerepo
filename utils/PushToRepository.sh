#!/bin/bash

OUTPUT_DIR="$1"
if [ -z "$OUTPUT_DIR" ];then
  OUTPUT_DIR="/var/www/html/repos/fedora/17/x86_64"
fi

if [ ! -d x86_64 ];then
  echo "Go to rpmbuild/RPMS"
  exit 1
fi

if [ -z "$OUTPUT_DIR" ];then
  echo "Error: No arguments!!!"
  echo "Set output path!!! eg. /var/www/html/repos/fedora/17/x86_64"
  exit 2
fi

if [ ! -d "$OUTPUT_DIR" ];then
  echo "$1 is not directory !!!"
  echo "Set output path!!! eg. /var/www/html/repos/fedora/17/x86_64"
  exit 3
fi

echo "Moving rpms to $OUTPUT_DIR/"
mv */* $OUTPUT_DIR/ > /dev/null 2>&1

if [ "$?" != "0" ];then
  echo "Nothing to copy !!!"
  exit 0
fi

createrepo $OUTPUT_DIR

#echo "Doing 'chcon -R -h -t httpd_sys_content_t /var/www/html' ..."
#chcon -R -h -t httpd_sys_content_t /var/www/html
#echo "Done"

