#!/usr/bin/env python3

from setuptools import setup, find_packages

setup(
    name='arpwitch',
    version='2017.2',
    description='A modern arpwatch tool',

    classifiers=[
        'Environment :: Console',
        'Intended Audience :: System Administrators',
        'Intended Audience :: Information Technology',
        'Topic :: System :: Networking :: Monitoring',
        'License :: OSI Approved :: Apache Software License',
    ],
    keywords='arpwitch arpwatch arp network',

    author='Nicholas de Jong',
    author_email='me(at)nicholasdejong.com',
    url='https://github.com/ndejong/arpwitch',
    license='Apache',

    packages=['arpwitch'],
    scripts=['bin/arpwitch'],
    install_requires=['scapy-python3'],

)
