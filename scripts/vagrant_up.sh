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

mkdir /home/vagrant/temp

sudo mkdir /var/lib/cassandra
sudo mkdir /var/log/cassandra
sudo chown -R vagrant /var/lib/cassandra
sudo chown -R vagrant /var/log/cassandra

sudo wget -O /home/vagrant/temp/apache-cassandra-2.0.9-bin.tar.gz http://psg.mtu.edu/pub/apache/cassandra/2.0.9/apache-cassandra-2.0.9-bin.tar.gz
sudo tar -xvzf /home/vagrant/temp/apache-cassandra-2.0.9-bin.tar.gz -C /home/vagrant/temp
sudo mv /home/vagrant/temp/apache-cassandra-2.0.9 /home/vagrant/cassandra

echo 'export CASSANDRA_HOME=/home/vagrant/cassandra' >> /home/vagrant/.bashrc
echo 'export PATH=$PATH:$CASSANDRA_HOME/bin' >> /home/vagrant/.bashrc

sh /home/vagrant/cassandra/bin/cassandra

echo "Waiting for Cassandra to start.."
sleep 10

sh /home/vagrant/cassandra/bin/cqlsh -e "create keyspace test WITH REPLICATION = { 'class' : 'SimpleStrategy', 'replication_factor' : 3 };"
