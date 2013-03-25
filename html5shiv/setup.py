"""
Python packaging definition.

It downloads the JS and CSS Files from upstream website
and creates a package.
"""

from distutils import log
from setuptools import setup, Command
import os
import shutil

NAME = 'chevah-weblibs-html5shiv'
VERSION = '3.6.2pre'
CHEVAH_VERSION = '-chevah2'
DOWNLOADS = [
    ('https://raw.github.com/aFarkas/html5shiv/%(version)s/dist/html5shiv.js',
        'chevah/weblibs/html5shiv/html5shiv.min.js'),
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
    author='html5shiv Team',
    maintainer="Adi Roiban",
    maintainer_email="adi.roiban@chevah.com",
    license='MIT',
    platforms='any',
    description='Files for html5shiv used in Chevah project.',
    long_description=open('README.rst').read(),
    url='https://github.com/aFarkas/html5shiv',
    namespace_packages=['chevah', 'chevah.weblibs'],
    packages=['chevah', 'chevah.weblibs', 'chevah.weblibs.html5shiv'],
    package_data=find_package_data(['chevah.weblibs.html5shiv']),
    cmdclass={
        'publish': PublishCommand,
        },
    )
