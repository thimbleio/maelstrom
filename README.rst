Maelstrom 
=========
.. image:: https://travis-ci.org/gradfly/maelstrom.svg?branch=develop
    :target: https://travis-ci.org/gradfly/maelstrom

A model based database library for Apache Cassandra built on top of DataStax Python Driver. This library has tested support for Python 2.7.

Installation
------------
Installing through pip is recommended:
::

    $ pip install maelstrom-py

You must have setuptools installed prior to installation. To install the package manually please refer to our installation guide. 

Get Started
-----------
Example usage of Maelstrom:

.. code-block:: python

    from uuid import uuid4
    import maelstrom
    from maelstrom.base import Base
	  from maelstrom.lookup import import LookUp

   	#ip1 and ip2 are IP address of some, but not necessarily all, nodes of your Cassandra cluster. 
    maelstrom.start([ip1, ip2])
    
    class User(Base):
    
      __tablename__ = "users"
      
      defaults = {
        'id' = uuid4(),
        'name' = '',
        'email' = '',
      }
      
      lookups = ["email"]
      
      def __init__(self, *args, **kwargs):
        self.update_data(**self.defaults)
        Base.__init__(self, *arks, **kwargs)
        
	  #constructs table in the specified keyspace
	  User.build()         
  	LookUp.build()

    new_user = User(name = "Joe", email="example@email.com")
    new_user.commit()
    
    get_user = Account.get_by_lookup("example@email.com")
    
    maelstrom.stop()

Documentation
-------------
TODO

License
-------
Copyright 2014 Matt Morse, Joe Peacock and contributors

Maelstrom is licensed under the `MIT License <https://github.com/gradfly/maelstrom/README.rst/>`_. 
