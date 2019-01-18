#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = ['Click>=7.0',
                'toml==0.10.0',
                'twilio==6.22.0',
                'sendgrid>=5.6.0'
                ]


setup_requirements = [ ]

test_requirements = [ ]

setup(
    author="arlenk",
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.6',
    ],
    description="send alerts (sms, email, etc.) when a client connects to your pivpn/openvpn server",
    entry_points={
        'console_scripts': [
            'pivpn_monitor=pivpn_monitor.cli:main',
        ],
    },
    install_requires=requirements,
    license="MIT license",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='pivpn_monitor',
    name='pivpn_monitor',
    packages=find_packages(),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/arlenk/pivpn_monitor',
    version='0.1.0',
    zip_safe=False,
)
