from distutils.core import setup

setup(name='maelstrom',
      version='0.1.0',
      author='Matt Morse, Joe Peacock',
      author_email='mmorse1217@gmail.com, joeapeacock@gmail.com',
      packages=['cassandra', 'cassandra.tests'],
      url='http://pypi.python.org/pypi/Maelstrom',
      license='LICENSE',
      description='A powerful, model based Cassandra wrapper for Python.',
      long_description=open('README.rst').read(),
      install_requires=[
          "cassandra-driver == 2.0.2"
      ])
