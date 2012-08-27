#!/bin/bash
#
# because of SELinux
#

echo "Doing 'chcon -R -h -t httpd_sys_content_t /var/www/html' ..."
chcon -R -h -t httpd_sys_content_t /var/www/html
echo "Done"
