from setuptools import setup, find_packages
import os


setup(
    name='argus',
    version='1.0.0',
    description='Argus CLI is a operational tool to maintain a personal homelab',
    license='MIT',

    author='Dave Pinhas',
    author_email='davepinhas89@gmail.com',
    url='ssh://git@github.com:davidpinhas/argus.git',

    classifiers=[
        'Programming Language :: Python :: 3.10'
    ],

    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'argus = cli.argus:main'
        ]
    },

    install_requires=[
        'click',
        'oci'
    ],
)
