from setuptools import setup

setup(name='maelstrom-py',
      version='0.1.32',
      author='Matt Morse, Joe Peacock',
      author_email='mmorse1217@gmail.com, joeapeacock@gmail.com',
      packages=['maelstrom', 'maelstrom.tests'],
      url='https://github.com/gradfly/maelstrom',
      license='LICENSE',
      description='A powerful, model based Cassandra wrapper for Python.',
      long_description=open('README.rst').read(),
      install_requires=[
          "cassandra-driver == 2.0.2",
          "nose >= 1.3.1",
          "rednose"
      ],
      test_suite="nose.collector")
