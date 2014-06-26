from setuptools import setup, find_packages

setup(	name='maelstrom',
		version='0.1',
		author='Matt Morse',
		author_email='matt@gradf.ly',
		packages=find_packages(),
		install_requires=['cassandra-driver'])
