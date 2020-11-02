#
# To update this, manually download the Win32 version from https://nssm.cc
# Update the name using Resource Hacker http://angusj.com/resourcehacker/
# Rename it to build/sftpplus-service-manager.exe
from setuptools import setup, Command
import os

NAME = 'chevah-nssm'
MODULE_NAME = 'nssm'
VERSION = '2.24.103'
CHEVAH_VERSION = '.chevah1'
WEBSITE = 'http://nssm.cc/'
AUTHOR = 'NSSM Team'
LICENSE = 'Public Domain'


class PublishCommand(Command):
    """
    Publish the source distribution to local pypi cache and remote
    Chevah PyPi server.
    """
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


def find_package_data(modules):
    """
    Returns the static dictionary of data files.
    """
    result = {}
    for module in modules:
        result.update({
            module: ['*.exe']})
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
    scripts=[
        'build/sftpplus-service-manager.exe',
        ],
    cmdclass={
        'publish': PublishCommand,
        },
    )
