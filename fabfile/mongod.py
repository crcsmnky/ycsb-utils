from fabric.api import *

MONGODBREPO = """
[mongodb]
name=MongoDB Repository
baseurl=http://downloads-distro.mongodb.org/repo/redhat/os/x86_64/
gpgcheck=0
enabled=1
"""

@task
@parallel
@roles('mongos', 'mongod', 'config')
def install():
    sudo('echo {repo} > /etc/yum.repos.d/mongodb.repo'.format(repo=MONGODBREPO))
    sudo('yum install -y mongodb-org')
    sudo('chkconfig mongod off')

@task
@parallel
@roles('mongod')
def setup():
    sudo('mkdir -p /data')
    sudo('chown mongod:mongod /data')
    sudo('echo dbpath=/data > /etc/mongod.conf')
    sudo('echo logpath=/var/log/mongod.log >> /etc/mongod.conf')
    sudo('echo fork=true >> /etc/mongod.conf')

@task
@parallel
@roles('mongod')
def start():
    sudo('service mongod start')

@task
@parallel
@roles('mongod')
def stop():
    sudo('service mongod stop')

@task
@parallel
@roles('mongod')
def getreadahead():
    sudo('blockdev --report')

@task
@parallel
@roles('mongod')
def setreadahead(ra=32, dev='/dev/xvdf'):
    sudo('blockdev --setra {ra} {dev}'.format(ra=ra, dev=dev))

@task
@parallel
@roles('mongod')
def getulimits():
    run('ulimit -a')

@task
@parallel
@roles('mongod')
def setulimits():
    sudo('echo "mongod soft nofile 64000" >> /etc/security/limits.conf')
    sudo('echo "mongod hard nofile 64000" >> /etc/security/limits.conf')
    sudo('echo "mongod soft nproc 32000" >> /etc/security/limits.conf')
    sudo('echo "mongod hard nproc 32000" >> /etc/security/limits.conf')

@task
@parallel
@roles('mongod')
def setkeepalive():
    sudo('echo "net.ipv4.tcp_keepalive_time = 300" >> /etc/sysctl.conf')
    sudo('echo 300 > /proc/sys/net/ipv4/tcp_keepalive_time')

@task
@parallel
@roles('mongod')
def setzonereclaim():
    sudo('echo 0 > /proc/sys/vm/zone_reclaim_mode')

