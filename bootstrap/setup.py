"""
Python packaging definition for AngularJS files.

It downloads the minified file from AngularJS website and creates a package.
"""

from distutils import log
from setuptools import setup, Command
import os
import shutil

NAME = 'chevah-weblibs-bootstrap'
VERSION = '2.2.2'
CHEVAH_VERSION = '.c3'


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


def find_package_data(modules):
    """
    Returns the static dictionary of data files.

    TODO: add dynamic code.
    """
    result = {}
    for module in modules:
        result.update({
            module: [
                'css/*',
                'img/*',
                'js/*',
                'less/*',
                ]})
    return result


setup(
    name=NAME,
    version=VERSION + CHEVAH_VERSION,
    author='Bootstrap Team',
    maintainer="Adi Roiban",
    maintainer_email="adi.roiban@chevah.com",
    license='Apache 2.0',
    platforms='any',
    description='Files for Twitter Bootstrap used in Chevah project.',
    long_description=open('README.rst').read(),
    url='http://twitter.github.com/bootstrap/',
    namespace_packages=['chevah', 'chevah.weblibs'],
    packages=['chevah', 'chevah.weblibs', 'chevah.weblibs.bootstrap'],
    package_data=find_package_data(['chevah.weblibs.bootstrap']),
    cmdclass={
        'publish': PublishCommand,
        },
    )
