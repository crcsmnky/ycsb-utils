from fabric.api import *
import ycsb
import mongos
import mongod
import config

env.roledefs = {
    'mongod': open('hosts/mongoshosts', 'r').read().splitlines(),
    'mongos': open('hosts/mongoshosts', 'r').read().splitlines(),
    'config': open('hosts/mongoshosts', 'r').read().splitlines(),
    'client': open('hosts/clienthosts', 'r').read().splitlines()
}

@task
def mongodbsetup():
    execute(mongod.install)
    execute(mongod.setup)

@task
def configureshardsystems(ra=32, dev='/dev/xvdf'):
    execute(mongod.setulimits)
    execute(mongod.setkeepalive)
    execute(mongod.setzonereclaim)
    execute(mongod.setreadahead, ra=ra, dev=dev)

@task
def setupclients():
    execute(ycsb.package)
    execute(ycsb.install)

