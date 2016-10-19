"""
Python packaging definition for WinSCP files.

Download the WinSCP zip and place it in /tmp
"""

from setuptools import setup, Command
import os
import shutil
import urllib2
import zipfile

NAME = 'chevah-testtools-winscp'
MODULE_NAME = 'winscp'
VERSION = '5.9.2'
CHEVAH_VERSION = '.chevah1'
WEBSITE = 'https://winscp.net'
AUTHOR = 'Martin Prikryl.'
LICENSE = 'GPL'


DIST_ZIP = 'tmp/WinSCP-%(version)s-Portable.zip' % {'version': VERSION}
FILES = ['WinSCP.com', 'WinSCP.exe']
PACKAGE_FILES = []
PACKAGE_FOLDER = 'chevah/testtools/winscp/'


def download():

    # Extract files.
    with zipfile.ZipFile(DIST_ZIP, 'r') as zip_file:
        zip_file.extractall('tmp/')

    # Copy distributable files.
    for component in FILES:
        source = 'tmp/%s' % (component,)
        destination = '%s/%s' % (PACKAGE_FOLDER, component)
        shutil.copy(source, destination)
        PACKAGE_FILES.append(destination)



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
        download()
        self.run_command('sdist')
        self.distribution.get_command_obj('sdist')

        # Upload package to Chevah PyPi server.
        upload_command = self.distribution.get_command_obj('upload')
        upload_command.repository = u'chevah'
        #self.run_command('upload')

        print 'Removing temporary folder'
        #shutil.rmtree('tmp/')
        for file in PACKAGE_FILES:
            os.unlink(file)


def find_package_data(modules):
    """
    Returns the static dictionary of data files.
    """
    result = {}
    for module in modules:
        result.update({
            module: [
                '*.exe',
                '*.com',
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
    namespace_packages=['chevah', 'chevah.testtools'],
    packages=['chevah', 'chevah.testtools', 'chevah.testtools.' + MODULE_NAME],
    package_data=find_package_data(['chevah.testtools.' + MODULE_NAME]),
    cmdclass={
        'publish': PublishCommand,
        },
    )
