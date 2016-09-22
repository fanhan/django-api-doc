# -*- coding:utf-8 -*-

import os
from distutils.core import setup
from django_api_doc import __version__


def get_packages(package):
    """
    Return root package and all sub-packages.
    """
    return [dirpath
            for dirpath, dirnames, filenames in os.walk(package)
            if os.path.exists(os.path.join(dirpath, '__init__.py'))]


def get_package_data(package):
    """
    Return all files under the root package, that are not in a
    package themselves.
    """
    walk = [(dirpath.replace(package + os.sep, '', 1), filenames)
            for dirpath, dirnames, filenames in os.walk(package)
            if not os.path.exists(os.path.join(dirpath, '__init__.py'))]

    filepaths = []
    for base, filenames in walk:
        filepaths.extend([os.path.join(base, filename)
                          for filename in filenames])
    return {package: filepaths}

setup(
    name='django_api_doc',
    version=__version__,
    description='API docs for django',
    long_description=open("README.md").read(),
    author='leavesfan',
    author_email='leavesfan@gmail.com',
    packages=get_packages('django_api_doc'),
    package_data=get_package_data('django_api_doc'),
    license="BSD",
    url='https://github.com/fanhan/django-api-doc'
)
