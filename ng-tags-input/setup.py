"""
Python packaging definition for AngularJS files.

It downloads the minified file from AngularJS website and creates a package.
"""

from distutils import log
from setuptools import setup, Command
import os
import shutil

NAME = 'chevah-weblibs-ng-tags-inputs'
MODULE_NAME = 'ng_tags_input'
VERSION = '2.1.1'
CHEVAH_VERSION = '.c1'
WEBSITE = 'https://github.com/mbenford/ngTagsInput/'

BASE_URL = (
    'https://github.com/mbenford/ngTagsInput/releases/download/'
    'v%(version)s/ng-tags-input.zip') % {'version': VERSION}
BASE_PATH = 'chevah/weblibs/%s/' % (MODULE_NAME)
DOWNLOADS = []

def add_version(name):
    if name.endswith('.min.js'):
        return name[:-7] + '-' + VERSION + '.min.js'
    if name.endswith('.js'):
        return name[:-3] + '-' + VERSION + '.js'
    if name.endswith('.min.css'):
        return name[:-8] + '-' + VERSION + '.min.css'
    if name.endswith('.css'):
        return name[:-4] + '-' + VERSION + '.css'
    return name


def download():
    """
    Download files.
    """
    import urllib2
    import zipfile
    from StringIO import StringIO
    print "Getting %s" % (BASE_URL,)
    web_handler = urllib2.urlopen(BASE_URL)
    with zipfile.ZipFile(StringIO(web_handler.read()), 'r') as archive:
        for name in archive.namelist():
            local = BASE_PATH + add_version(name)
            output = open(local, 'wb')
            DOWNLOADS.append(local)
            output.write(archive.read(name))
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

    def finalize_options(self):
        self.cwd = os.getcwd()

    def run(self):
        assert os.getcwd() == self.cwd, (
            'Must be in package root: %s' % self.cwd)
        download()
        self.run_command('sdist')

        # Upload package to Chevah PyPi server.
        upload_command = self.distribution.get_command_obj('upload')
        upload_command.repository = u'chevah'
        self.run_command('upload')

        # Delete temporary files downloaded only for building the package.
        for local in DOWNLOADS:
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
    author='Michael Benford',
    maintainer="Adi Roiban",
    maintainer_email="adi.roiban@chevah.com",
    license='MIT',
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
