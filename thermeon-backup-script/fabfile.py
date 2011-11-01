import re
import os
import fileinput



#
#  Try to load the fabric libraries and catch any error.
#
try:
    from fabric.api import *
    from fabric.contrib.console import confirm
except ImportError:
    print ("""The 'fabric' package is currently not installed. You can install it by typing:\n
sudo apt-get install fabric
""")
    sys.exit()





#
#  TODO make better
#
env.user = 'bytemark'
env.hosts  = [ 'thermeon-v1a.dh.bytemark.co.uk', 'thermeon-v1b.dh.bytemark.co.uk', 'thermeon-v2a.dh.bytemark.co.uk', 'thermeon-v2b.dh.bytemark.co.uk', 'thermeon-v3a.dh.bytemark.co.uk', 'thermeon-v3b.dh.bytemark.co.uk' ]



def hostname():
   """
   Test that the connection to the deployed host works.
   """
   run( "hostname --fqdn" )


def maxfiles():
   """
   Increase the limit of open files.
   """
   sudo( "sysctl -w fs.file-max=1000000", pty=True)


def deploy():
   """
   Upload the backup script.
   """
   put( "backup.script", "/tmp/script" )
   sudo( "mv /tmp/script /usr/local/sbin/backup.script", pty=True )
   sudo( "chown root.root  /usr/local/sbin/backup.script", pty=True )
   sudo( "chmod 755        /usr/local/sbin/backup.script", pty=True )
