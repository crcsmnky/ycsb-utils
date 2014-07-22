from fabric.api import *
from datetime import datetime
import time

@task
@runs_once
@roles('client')
def package():
    local('mvn clean package')

@task
@parallel
@roles('client')
def install():
    put('YCSB/distribution/target/ycsb-0.1.4.tar.gz', '~/ycsb.tar.gz')
    run('tar xvf ~/ycsb.tar.gz')

def syncworkloads():
    run('mkdir -p ~/workloads')
    put('workloads/*', '~/workloads/')
    run('mkdir -p ~/datasets')
    put('datasets/*', '~/datasets/')

@runs_once
@roles('client')
def recordcount(dataset):
    return local('awk -F"=" \' /recordcount/ {print $2}\' {dataset}'
        .format(dataset=dataset), capture=True)

@task
@roles('client')
def load(dataset, workload):
    execute(syncworkloads)

    numclients = len(env.roledefs['client'])
    count = recordcount(workload)

    insertcount = count / numclients
    insertstart = insertcount * env.roledefs['client'].index(env.host)

    cmd =  '~/ycsb-0.1.4/bin/ycsb load mongodb'
    cmd += ' -P {dataset}'.format(dataset)
    cmd += ' -P {workload}'.format(workload)
    cmd += ' -p insertstart={start}'.format(insertstart)
    cmd += ' -p insertcount={count}'.format(insertcount)
    cmd += ' -p mongodb.url=localhost'
    cmd += ' -threads 32'
    cmd += ' > load.out 2> load.err'

    run(cmd)

@task
@parallel
@roles('client')
def run(dataset, workload):
    execute(syncworkloads)

    cmd =  '~/ycsb-0.1.4/bin/ycsb run mongodb'
    cmd += ' -P {dataset}'.format(dataset)
    cmd += ' -P {workload}'.format(workload)
    cmd += ' -p mongodb.url=localhost:27017'
    cmd += ' -threads 32'
    cmd += ' > run.out 2> run.err'

    run(cmd)

timestamp = datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')

@task
@roles('client')
def processlogs():
    execute(loadlogs, timestamp=timestamp)
    execute(runlogs, timestamp=timestamp)
    execute(summarizelogs, timestamp=timestamp)

@parallel
@roles('client')
def loadlogs(timestamp):
    clientid = env.roledefs['client'].index(env.host)
    local_out = 'output/{timestamp}/{clientid}-load.out'.format(
        timestamp=timestamp,clientid=clientid)
    local_err = 'output/{timestamp}/{clientid}-load.err'.format(
        timestamp=timestamp,clientid=clientid)
    get('load.out',local_out)
    get('load.err',local_err)

@parallel
@roles('client')
def runlogs(timestamp):
    clientid = env.roledefs['client'].index(env.host)
    local_out = 'output/{timestamp}/{clientid}-run.out'.format(
        timestamp=timestamp,clientid=clientid)
    local_err = 'output/{timestamp}/{clientid}-run.err'.format(
        timestamp=timestamp,clientid=clientid)
    get('run.out',local_out)
    get('run.err',local_err)

@runs_once
@roles('client')
def summarizelogs(timestamp):
    rtp = local('awk \'/Throughput/ {sum += $3} END {print sum} \' ./output/{timestamp}/*run.out'.format(
        timestamp), capture=True)
    print('Run Throughput: {rtp}'.format(rtp))

    ltp = local('awk \'/Throughput/ {sum += $3} END {print sum} \' ./output/{timestamp}/*load.out'.format(
        timestamp), capture=True)
    print('Load Throughput: {ltp}'.format(ltp))

