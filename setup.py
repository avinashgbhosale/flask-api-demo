# - coding: utf-8 --

from setuptools import setup, find_packages

requires = [
    'Flask',
    'Flask-RESTX',
    'boto3',
    'requests'
]

setup(
    name='Flask API',
    version='1.0',
    description='Flask API',
    author='Avinash Bhosale',
    author_email='bhosaleavinash22@gmail.com',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=requires,
    tests_require=requires,
)
