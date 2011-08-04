import os
from setuptools import setup

version = "1.0"

setup(
    name='mr.hermes',
    version=version,
    description="A simple debug smtp server for development.",
    long_description=open("README.rst").read() + "\n\n" +
                     open(os.path.join("HISTORY.txt")).read(),
    author='Florian Schulze',
    author_email='florian.schulze@gmx.net',
    url='http://github.com/fschulze/mr.hermes',
    packages=['mr'],
    namespace_packages=['mr'],
    zip_safe=True,
    install_requires=[
        'setuptools'])
