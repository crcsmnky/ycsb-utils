from fabric.api import *

@task
@parallel
@roles('mongos')
def start():
    run('/usr/bin/mongos --fork --logpath ~/mongos.log --configdb {confighosts}'
        .format(confighosts=','.join(env.roledefs['config'])))

@task
@runs_once
@roles('mongos')
def addshards():
    for m in env.roledefs['mongod']:
        run('/usr/bin/mongo --eval "sh.addShard(\'{mongodhost}:27017\')"'
            .format(mongodhost=m))

@task
@runs_once
@roles('mongos')
def initsharding():
    put('scripts/presplit.js', '~/presplit.js')
    run('/usr/bin/mongo ~/presplit.js')
