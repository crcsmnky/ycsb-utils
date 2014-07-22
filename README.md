# YCSB Utilities

A set of [Fabric](http://www.fabfile.org/) scripts to simplify the deployment and execution of YCSB testing with MongoDB.

Inspired by, but not a direct fork of, [Jared's YCSB Tools](https://github.com/jsr/ycsb-tools).

## Basics

    $ pip install -r requirements.txt
    $ fab --list
    Available commands:

        configureshardsystems
        mongodbsetup
        setupclients
        config.setup
        config.start
        config.stop
        mongod.getreadahead
        mongod.getulimits
        mongod.install
        mongod.setkeepalive
        mongod.setreadahead
        mongod.setulimits
        mongod.setup
        mongod.setzonereclaim
        mongod.start
        mongod.stop
        mongos.addshards
        mongos.initsharding
        mongos.start
        ycsb.install
        ycsb.load
        ycsb.package
        ycsb.processlogs
        ycsb.run

## Setup

First edit the appropriate `hosts` files and enter in the hostnames for each component.

    $ fab mongodbsetup
    $ fab configureshardsystems:ra=32,dev=/dev/xvdf
    $ fab setupclients
    $ fab config.setup
    $ fab mongos.start
    $ fab mongos.addshards
    $ fab mongos.initsharding

## Execute

    $ fab ycsb.load:dataset=1gb,workload=read-only
    $ fab ycsb.run:dataset=1gb,workload=read-only
    $ fab ycsb.processlogs