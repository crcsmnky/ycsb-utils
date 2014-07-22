var db = db.getSiblingDB("ycsb");
var ns = "ycsb.usertable";
var shards = db.getSiblingDB("config").shards.find();
var numShards = shards.length();
var shardNames = [];

print("Setup Database Sharding");
sh.enableSharding("ycsb");
sh.shardCollection(ns, {"_id": 1});

print("Disable the Balancer");
sh.disableBalancing(ns);

for(var s = 0; s < shards.length(); s++) {
    shardNames.push(shards[s]._id);
}

print("Setup Pre Splits");

for(i = 0; i < 1000; i = i + 5) {
    var prefix = "user" + String(i);
    print("Chunk " + prefix);
    var result = db.adminCommand({split: ns, middle: {_id: prefix}});
    printjson(result);
}

print("Moving Chunks");

for(i = 0; i < 1000; i = i + 5) {
    var prefix = "user" + String(i);
    var dest = shardNames[i % numShards];
    print("Moving chunk: " + prefix + " to shard " + dest);
    result = sh.moveChunk(ns, {_id: prefix}, dest);
    printjson(result);
}

print("Disable Power of 2");
db.runCommand({"collMod": "usertable", "usePowerOf2Sizes": false});

print("Enable the Balancer");
sh.enableBalancing(ns);


