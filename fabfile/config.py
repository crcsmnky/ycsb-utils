from fabric.api import *

@task
@parallel
@roles('config')
def setup():
    sudo('echo dbpath=/data > /etc/mongod.conf')
    sudo('echo logpath=/var/log/config.log >> /etc/mongod.conf')
    sudo('echo fork=true >> /etc/mongod.conf')
    sudo('echo configsvr=true >> /etc/mongod.conf')

@task
@parallel
@roles('config')
def start():
    sudo('service mongod start')

@task
@parallel
@roles('config')
def stop():
    sudo('service mongod stop')
