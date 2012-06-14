yum remove alice\*
# rpm -qa --queryformat="%{NAME}\n" | grep "alice-" | xargs rpm -e
