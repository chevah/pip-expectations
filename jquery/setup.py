"""
Python packaging definition for jQuery files.

It downloads the minified file from jQuery website and creates a package.
"""

from distutils import log
from setuptools import setup, Command
import os
import shutil

NAME = 'chevah-weblibs-jquery'
VERSION = '1.8.3'
CHEVAH_VERSION = '-chevah1'
DOWNLOAD_URL = 'http://code.jquery.com/jquery-%(version)s.min.js'
LOCAL_FILE = 'chevah/weblibs/jquery/jquery.min.js'


def download():
    """
    Download minified JS file.
    """
    import urllib2
    url = DOWNLOAD_URL % {'version': VERSION}
    mp3file = urllib2.urlopen(url)
    output = open(LOCAL_FILE, 'wb')
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

        # Delete temporary file downloaded only for building the package.
        os.remove(LOCAL_FILE)


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
    name=NAME,
    version=VERSION + CHEVAH_VERSION,
    maintainer="Adi Roiban",
    maintainer_email="adi.roiban@chevah.com",
    license='Same as jQuery',
    platforms='any',
    description='Files for JQuery used in Chevah project.',
    long_description=open('README.rst').read(),
    url='http://jquery.com/',
    namespace_packages=['chevah', 'chevah.weblibs'],
    packages=['chevah', 'chevah.weblibs', 'chevah.weblibs.jquery'],
    package_data=find_package_data(['chevah.weblibs.jquery']),
    cmdclass={
        'publish': PublishCommand,
        },
    )
