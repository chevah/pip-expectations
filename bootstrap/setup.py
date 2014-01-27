"""
Python packaging definition for AngularJS files.

It downloads the minified file from AngularJS website and creates a package.
"""

from setuptools import setup, Command
import os

NAME = 'chevah-weblibs-bootstrap'
VERSION = '2.3.2'
CHEVAH_VERSION = '.c1'


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
