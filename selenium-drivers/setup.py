"""
Python packaging definition for Selenium Drivers files.

Drivers need to be manually downloaded and extracted into the `drivers` folder
and renamed as defined in setup.py.

Download IE drivers from
http://www.seleniumhq.org/download/ (The Internet Explorer Driver Server)

Download Chrome drivers from
https://sites.google.com/chromium.org/driver/

Download Firefox drivers from
https://github.com/mozilla/geckodriver/releases

File names:
* geckodriver-linux-64
* chromedriver-linux-64
"""
from setuptools import setup, Command
import os

NAME = 'chevah-selenium-drivers'
MODULE_NAME = b'selenium_drivers'
# ChromeDriver 98.0.4758.48
# Firefox 0.30.0
# The drivers version are following the Selenium version.
VERSION = '3.141.0'
CHEVAH_VERSION = '+chevah.7'
WEBSITE = 'http://docs.seleniumhq.org/'
AUTHOR = 'Selenium Contributors'
LICENSE = 'Apache 2.0'


setup(
    name=NAME,
    version=VERSION + CHEVAH_VERSION,
    author=AUTHOR,
    author_email='hidden',
    maintainer="Adi Roiban",
    maintainer_email="adi.roiban@chevah.com",
    license=LICENSE,
    platforms='any',
    description='Files for %s used in Chevah project.' % (MODULE_NAME),
    long_description=open('README.rst').read(),
    url=WEBSITE,
    namespace_packages=['chevah'],
    packages=['chevah', MODULE_NAME],
    package_dir={MODULE_NAME: 'chevah/' + MODULE_NAME},
    package_data={MODULE_NAME: ['*']},
    )
