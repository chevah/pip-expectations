"""
Python packaging definition for Selenium Drivers files.
"""
from setuptools import setup, Command
import os

NAME = 'chevah-selenium-drivers'
MODULE_NAME = b'selenium_drivers'
# ChromeDriver 88.0.4324.27
# Firefox 0.28.0
# The drivers version are following the Selenium version.
VERSION = '3.141.0'
CHEVAH_VERSION = '.chevah5'
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
        self.run_command('bdist_wheel')
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
    packages=[b'chevah', b'chevah.' + MODULE_NAME],
    scripts=[
        b'drivers/chromedriver-linux-64',
        b'drivers/geckodriver-linux-64',
        ],
    cmdclass={
        'publish': PublishCommand,
        },
    )
