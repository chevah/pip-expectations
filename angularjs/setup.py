"""
Python packaging definition for AngularJS files.

It downloads the minified file from AngularJS website and creates a package.
"""

from distutils import log
from setuptools import setup, Command
import os
import shutil

NAME = 'chevah-weblibs-angularjs'
VERSION = '1.1.2'
CHEVAH_VERSION = '-chevah1'

BASE_URL = 'http://code.angularjs.org/%(version)s/'
BASE_PATH = 'chevah/weblibs/angularjs/'
FILES = [
    'angular.js',
    'angular.min.js',
    'angular-bootstrap-prettify.min.js',
    'angular-bootstrap.min.js',
    'angular-cookies.min.js',
    'angular-mocks.js',
    'angular-loader.min.js',
    'angular-resource.min.js',
    'angular-sanitize.js',
    'angular-sanitize.min.js',
    'angular-scenario.js',
    'jstd-scenario-adapter-config.js',
    'jstd-scenario-adapter.js',
    ]

DOWNLOADS = []
for filename in FILES:
    DOWNLOADS.append((BASE_URL + filename, BASE_PATH + filename))


def download():
    """
    Download files.
    """
    import urllib2
    for remote, local in DOWNLOADS:
        url = remote % {'version': VERSION}
        print "Getting %s into %s" % (url, local)
        mp3file = urllib2.urlopen(url)
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
                ]})
    return result


setup(
    name='chevah-weblibs-angularjs',
    version=VERSION + CHEVAH_VERSION,
    maintainer="Adi Roiban",
    maintainer_email="adi.roiban@chevah.com",
    license='Same as AngularJS',
    platforms='any',
    description='Files for AngularJS used in Chevah project.',
    long_description=open('README.rst').read(),
    url='http://angularjs.org/',
    namespace_packages=['chevah', 'chevah.weblibs'],
    packages=['chevah', 'chevah.weblibs', 'chevah.weblibs.angularjs'],
    package_data=find_package_data(['chevah.weblibs.angularjs']),
    cmdclass={
        'publish': PublishCommand,
        },
    )
