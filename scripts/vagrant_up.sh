#!/usr/bin/env bash

apt-get update

#Why isn't this installed already...
apt-get install -y vim

# Installs
apt-get install -y python-dev
apt-get install -y make
apt-get install -y tcl8.5
apt-get install -y build-essential
apt-get install -y libpq-dev
apt-get install -y python-pip
apt-get install -y python-setuptools
apt-get install -y curl
apt-get install -y --force-yes dsc20
apt-get install -y libev4 libev-dev
apt-get install -y openjdk-7-jre
apt-get install -y openjdk-7-jdk

apt-get update

pip install virtualenv
virtualenv /vagrant/venv

source /vagrant/venv/bin/activate
pip install --upgrade setuptools
pip install -r /vagrant/scripts/requirements.txt
easy_install rednose
echo 'export NOSE_REDNOSE=1' >> /home/vagrant/.bashrc
deactivate -d

su vagrant

mkdir ~/temp
cd ~temp

sudo wget http://apache.tradebit.com/pub/~/2.0.9/apache-cassandra-2.0.9-bin.tar.gz
sudo tar -xvzf apache-cassandra-2.0.9-bin.tar.gz
sudo mv apache-cassandra-2.0.9 ~/cassandra

sudo mkdir /var/lib/cassandra
sudo mkdir /var/log/cassandra
sudo chown -R $USER:$GROUP /var/lib/cassandra
sudo chown -R $USER:$GROUP /var/log/cassandra

cassandra
cqlsh -e "create keyspace test WITH REPLICATION = { 'class' : 'SimpleStrategy', 'replication_factor' : 3 };"
