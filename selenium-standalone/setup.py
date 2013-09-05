"""
Python packaging definition for Selenium Standalone files.
"""

from distutils import log
from setuptools import setup, Command
import os
import shutil

NAME = 'chevah-selenium-standalone'
MODULE_NAME = 'selenium_standalone'
VERSION = '2.35.0'
CHEVAH_VERSION = '-1'
WEBSITE = 'http://docs.seleniumhq.org/'
AUTHOR = 'Selenium Contributors'
LICENSE = 'Apache 2.0'

BASE_URL = 'http://selenium.googlecode.com/files/'
BASE_PATH = 'chevah/%s/' % (MODULE_NAME)
FILES = [
    ('selenium-server-standalone-%(version)s.jar',
        'selenium-server-standalone.jar')]

DOWNLOADS = []
for remote_filename, local_filename in FILES:
    remote_filename = remote_filename % {'version': VERSION}
    remote = BASE_URL + remote_filename
    local = BASE_PATH + local_filename
    DOWNLOADS.append((remote, local))


def download():
    """
    Download files.
    """
    import urllib
    for remote, local in DOWNLOADS:
        print "Getting %s into %s" % (remote, local)
        urllib.urlretrieve(remote, local)


class PublishCommand(Command):
    """
    Publish the source distribution to local pypi cache and remote
    Chevah PyPi server.
    """

    description = "copy distributable to Chevah cache folder"
    user_options = []

    def initialize_options(self):
        self.cwd = None
        self.destination_base = '~/chevah/brink/cache/pypi/'

    def finalize_options(self):
        self.cwd = os.getcwd()

    def run(self):
        assert os.getcwd() == self.cwd, (
            'Must be in package root: %s' % self.cwd)
        download()
        self.run_command('sdist')
        sdist_command = self.distribution.get_command_obj('sdist')
        for archive in sdist_command.archive_files:
            source = os.path.join(archive)
            destination = os.path.expanduser(
                self.destination_base + os.path.basename(archive))
            shutil.copyfile(source, destination)
        log.info(
            "Distributables files copied to %s " % (self.destination_base))

        # Upload package to Chevah PyPi server.
        upload_command = self.distribution.get_command_obj('upload')
        upload_command.repository = u'chevah'
        self.run_command('upload')

        # Delete temporary files downloaded only for building the package.
        for remote, local in DOWNLOADS:
            os.remove(local)


def find_package_data(modules):
    """
    Returns the static dictionary of data files.

    TODO: add dynamic code.
    """
    result = {}
    for module in modules:
        result.update({
            module: [
                '*.jar',
                ]})
    return result


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
    package_data=find_package_data(['chevah.' + MODULE_NAME]),
    cmdclass={
        'publish': PublishCommand,
        },
    )
