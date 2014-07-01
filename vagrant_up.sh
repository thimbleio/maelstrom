#!/usr/bin/env bash

apt-get update

#Why isn't this installed already...
apt-get install -y vim

#General Python setup
apt-get install -y python-dev
apt-get install -y make
apt-get install -y tcl8.5
apt-get install -y build-essential
apt-get install -y libpq-dev
apt-get install -y python-pip
apt-get install -y python-setuptools

pip install virtualenv

virtualenv /vagrant/venv
source /vagrant/venv/bin/activate

pip install --upgrade setuptools
pip install -r /vagrant/requirements.txt

#C extensions for Cassandra
apt-get install -y libev4 libev-dev

easy_install rednose
echo 'export NOSE_REDNOSE=1' >> /home/vagrant/.bashrc

#Install Oracle JDK 7
apt-get install -y openjdk-7-jre 
apt-get install -y openjdk-7-jdk

deactivate

#Install Cassandra.... Let's hope this works...
echo "deb http://debian.datastax.com/community stable main" | sudo tee -a /etc/apt/sources.list.d/cassandra.sources.list
apt-get install -y curl
apt-get update
apt-get install -y --force-yes dsc20
cassandra
cqlsh -e "create keyspace test WITH REPLICATION = { 'class' : 'SimpleStrategy', 'replication_factor' : 3 };"
