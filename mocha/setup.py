"""
Python packaging definition for Mocha files.

It downloads the JS and CSS Files from Mocha github website
and creates a package.
"""

from distutils import log
from setuptools import setup, Command
import os
import shutil

NAME = 'chevah-weblibs-mocha'
VERSION = '1.8.1'
CHEVAH_VERSION = '-chevah1'
DOWNLOADS = [
    ('https://raw.github.com/visionmedia/mocha/%(version)s/mocha.js',
        'chevah/weblibs/mocha/mocha.js'),
    ('https://raw.github.com/visionmedia/mocha/%(version)s/mocha.css',
        'chevah/weblibs/mocha/mocha.css'),
    ]


def download():
    """
    Download file.
    """
    import urllib2
    for remote, local in DOWNLOADS:
        url = remote % {'version': VERSION}
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

        # Delete temporary file downloaded only for building the package.
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
    maintainer="Adi Roiban",
    maintainer_email="adi.roiban@chevah.com",
    license='Same as Mocha',
    platforms='any',
    description='Files for Mocha used in Chevah project.',
    long_description=open('README.rst').read(),
    url='http://visionmedia.github.com/mocha/',
    namespace_packages=['chevah', 'chevah.weblibs'],
    packages=['chevah', 'chevah.weblibs', 'chevah.weblibs.mocha'],
    package_data=find_package_data(['chevah.weblibs.mocha']),
    cmdclass={
        'publish': PublishCommand,
        },
    )