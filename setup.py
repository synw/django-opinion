import os
from setuptools import setup, find_packages

import polls


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name='django-opinion',
    version=polls.__version__,
    description='Polls application for Django',
    long_description=read('README.md'),
    license='MIT License',
    author='synwe',
    author_email='',
    url='https://github.com/synwe/django-opinion',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'Django',
    ],
)
