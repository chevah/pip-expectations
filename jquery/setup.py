"""
Python packaging definition for JQuery files.
"""

from distutils import log
from setuptools import setup, Command
import os
import shutil

NAME = 'chevah-weblibs-jquery'
MODULE_NAME = 'jquery'
VERSION = '1.10.1'
CHEVAH_VERSION = '-chevah2'
WEBSITE = 'http://jquery.com/'
AUTHOR = 'jQuery Foundation and other contributors'
LICENSE = 'MIT'


BASE_URL = (
    'http://code.jquery.com/')
BASE_PATH = 'chevah/weblibs/%s/' % (MODULE_NAME)
FILES = [
    'jquery-%s.js' % (VERSION),
    'jquery-%s.min.js' % (VERSION),
    ]


DOWNLOADS = []
for filename in FILES:
    remote = (BASE_URL + filename) % {'version': VERSION}
    local = BASE_PATH + filename
    DOWNLOADS.append((remote, local))


def download():
    """
    Download files.
    """
    import urllib2
    for remote, local in DOWNLOADS:
        print "Getting %s into %s" % (remote, local)
        mp3file = urllib2.urlopen(remote)
        output = open(local, 'wb')
        output.write(mp3file.read())
        output.close()


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
                '*.js',
                '*.css',
                ]})
    return result


setup(
    name=NAME,
    version=VERSION + CHEVAH_VERSION,
    author=AUTHOR,
    maintainer="Adi Roiban",
    maintainer_email="adi.roiban@chevah.com",
    license=LICENSE,
    platforms='any',
    description='Files for %s used in Chevah project.' % (MODULE_NAME),
    long_description=open('README.rst').read(),
    url=WEBSITE,
    namespace_packages=['chevah', 'chevah.weblibs'],
    packages=['chevah', 'chevah.weblibs', 'chevah.weblibs.' + MODULE_NAME],
    package_data=find_package_data(['chevah.weblibs.' + MODULE_NAME]),
    cmdclass={
        'publish': PublishCommand,
        },
    )
