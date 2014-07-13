1, Install MongoDB
#Mac OSX
curl -O http://downloads.mongodb.org/osx/mongodb-osx-x86_64-2.6.3.tgz
http://fastdl.mongodb.org/linux/mongodb-linux-x86_64-2.6.3.tgz
tar -zxvf mongodb-osx-x86_64-2.6.3.tgz
mkdir -p mongodb
cp -R -n mongodb-osx-x86_64-2.6.3/ mongodb
export PATH=<mongodb-install-directory>:$PATH

#Linux


2, Startup MongoDB
sudo mkdir -p /data/db
sudo chown chenjianjun /data/db
mongod

3, Testing Connection
>>> from mongoengine import *
>>> connect("pdlib")
MongoClient('localhost', 27017)