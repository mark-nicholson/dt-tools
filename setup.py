#
#  Generic setup script derived from Python.org doc pages.
#

from distutils.core import setup

setup(
    name='DeviceTree',
    version='0.1',
    author='Mark Nicholson',
    author_email='nicholson.mark@gmail.com',
    packages=['devicetree' ],
    url='http://pypi.python.org/pypi/dttools/',
    license='LICENSE',
    description='Flattened Device Tree parser and utilities.',
    long_description=open('README.md').read(),
)
