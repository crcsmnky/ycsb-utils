var dbName = "ycsb";

var db = db.getSiblingDB(dbName);
var ns = dbName + ".usertable";


print("Setup Database Sharding");
sh.enableSharding(dbName);
sh.shardCollection(ns, {"_id": "hashed"});

print("Disable Power of 2");
db.runCommand({"collMod": "usertable", "usePowerOf2Sizes": false});

