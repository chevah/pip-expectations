"""
Python packaging definition for AngularJS files.

It downloads the minified file from AngularJS website and creates a package.
"""

from distutils import log
from setuptools import setup, Command
import os
import shutil

NAME = 'chevah-weblibs-angular-ui-bootstrap'
MODULE_NAME = 'angular_ui_bootstrap'
VERSION = '0.3.0'
CHEVAH_VERSION = '-chevah1'
WEBSITE = 'http://angular-ui.github.com/bootstrap/'

BASE_URL = 'https://raw.github.com/angular-ui/bootstrap/gh-pages/'
BASE_PATH = 'chevah/weblibs/%s/' % (MODULE_NAME)
FILES = [
    'ui-bootstrap-tpls-0.3.0.min.js',
    'ui-bootstrap-tpls-0.3.0.js',
    ]


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

DOWNLOADS = []
for filename in FILES:
    remote = BASE_URL + filename
    local = BASE_PATH + filename
    DOWNLOADS.append((remote, local))


def download():
    """
    Download files.
    """
    import urllib2
    for remote, local in DOWNLOADS:
        print "Getting %s into %s" % (remote, local)
        mp3file = urllib2.urlopen(remote)
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
                '*.css',
                ]})
    return result


setup(
    name=NAME,
    version=VERSION + CHEVAH_VERSION,
    author='AngularUI Team',
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
