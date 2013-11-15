# -*- coding: utf-8 -*-
from setuptools import setup

setup(
    name='da-vinci',
    version='0.1.0',
    author='Selwin Ong',
    author_email='selwin.ong@gmail.com',
    packages=['da_vinci'],
    url='https://github.com/ui/da-vinci',
    license='MIT',
    description='A simple image manipulation library aiming to make common image tasks easy.',
    long_description=open('README.rst').read(),
    zip_safe=False,
    include_package_data=True,
    package_data={'': ['README.rst']},
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Multimedia :: Graphics'
    ]
)
