"""
Python packaging definition for Selenium Drivers files.
"""
from setuptools import setup, Command
import os

NAME = 'chevah-selenium-drivers'
MODULE_NAME = 'selenium_drivers'
VERSION = '2.39.0'  # ChromeDriver 2.8.
CHEVAH_VERSION = '-1'
WEBSITE = 'http://docs.seleniumhq.org/'
AUTHOR = 'Selenium Contributors'
LICENSE = 'Apache 2.0'


class PublishCommand(Command):
    """
    Publish the source distribution to local pypi cache and remote
    Chevah PyPi server.
    """

    description = "copy distributable to Chevah cache folder"
    user_options = []

    def initialize_options(self):
        self.cwd = None

    def finalize_options(self):
        self.cwd = os.getcwd()

    def run(self):
        assert os.getcwd() == self.cwd, (
            'Must be in package root: %s' % self.cwd)
        self.run_command('sdist')
        # Upload package to Chevah PyPi server.
        upload_command = self.distribution.get_command_obj('upload')
        upload_command.repository = u'chevah'
        self.run_command('upload')

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
    packages=['chevah', 'chevah.' + MODULE_NAME],
    scripts=[
        'drivers/chromedriver-linux-32',
        'drivers/chromedriver-linux-64',
        'drivers/chromedriver-windows-32.exe',
        'drivers/iedriver-windows-32.exe',
        'drivers/iedriver-windows-64.exe',
        ],
    cmdclass={
        'publish': PublishCommand,
        },
    )
