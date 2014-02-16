"""
Python packaging definition for Bootstrap files.
"""
from setuptools import setup, Command
import os
import shutil
import urllib2
import zipfile

NAME = 'chevah-weblibs-bootstrap'
VERSION = '3.1.1'
CHEVAH_VERSION = '.c1'
DIST_URL = (
    'https://github.com/twbs/bootstrap/releases/'
    'download/v%(version)s/bootstrap-%(version)s-dist.zip') % {
        'version': VERSION,
        }
SOURCE_URL = 'https://github.com/twbs/bootstrap/archive/v%(version)s.zip' % {
    'version': VERSION,
    }

DIST_ZIP = 'tmp/bootstrap-%(version)s-dist.zip' % {'version': VERSION}
SOURCE_ZIP = 'tmp/bootstrap-%(version)s.zip' % {'version': VERSION}

PACKAGE_FOLDER = 'chevah/weblibs/bootstrap/'

TEMP_FOLDERS = []

def download():
    print 'Creating temporary folder'
    base_temp = 'tmp'
    os.mkdir(base_temp)
    TEMP_FOLDERS.append(base_temp)

    download_file(DIST_URL, DIST_ZIP)
    download_file(SOURCE_URL, SOURCE_ZIP)

    # Extract files.
    with zipfile.ZipFile(DIST_ZIP, 'r') as zip_file:
        zip_file.extractall('tmp/')
    with zipfile.ZipFile(SOURCE_ZIP, 'r') as zip_file:
        zip_file.extractall('tmp/')

    # Copy distributable files.
    source_base = 'tmp/bootstrap-%(version)s-dist' % {'version': VERSION}
    for component in ['css', 'fonts', 'js']:
        source = '%s/%s' % (source_base, component)
        description = '%s/%s' % (PACKAGE_FOLDER, component)
        TEMP_FOLDERS.append(description)
        shutil.copytree(source, description)

    # Copy files from source.
    source_base = 'tmp/bootstrap-%(version)s' % {'version': VERSION}
    for component in ['less']:
        source = '%s/%s' % (source_base, component)
        description = '%s/%s' % (PACKAGE_FOLDER, component)
        TEMP_FOLDERS.append(description)
        shutil.copytree(source, description)

def download_file(url, path):
    """Get a file from web."""
    print "Downloading %s at %s" % (url, path)
    remote_file = urllib2.urlopen(url)
    output = open(path, 'wb')
    output.write(remote_file.read())
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
        # # Upload package to Chevah PyPi server.
        upload_command = self.distribution.get_command_obj('upload')
        upload_command.repository = u'chevah'
        self.run_command('upload')

        # Delete temporary file downloaded only for building the package.
        print 'Removing temporary folders:'
        for folder in TEMP_FOLDERS:
            print folder
            shutil.rmtree(folder)

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
                'fonsts/*',
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
