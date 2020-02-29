#!/usr/bin/env python3

from setuptools import setup, find_packages
from ArpWitch import NAME
from ArpWitch import VERSION

with open('README.md', 'r') as f:
    long_description = f.read()


setup(
    name=NAME,
    version=VERSION,
    description='A modern arpwatch replacement with JSON formatted outputs and easy options to exec commands when network changes are observed',

    long_description=long_description,
    long_description_content_type='text/markdown',

    classifiers=[
        'Environment :: Console',
        'Intended Audience :: System Administrators',
        'Intended Audience :: Information Technology',
        'Topic :: System :: Networking :: Monitoring',
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: BSD License',
    ],
    keywords='arpwitch arpwatch arp network',

    author='Verb Networks Pty Ltd',
    author_email='contact@verbnetworks.com',
    url='https://github.com/verbnetworks/arpwitch',
    license='BSD-2-Clause',

    zip_safe=False,
    packages=find_packages(),
    scripts=['bin/arpwitch'],

    install_requires=['scapy', 'ouilookup'],
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],

)
