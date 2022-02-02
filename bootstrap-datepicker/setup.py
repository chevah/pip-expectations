"""
Python packaging definition for one of the forks for
Bootstrap datetime picker files.
"""
from __future__ import print_function
from setuptools import setup, Command
import os
import ssl

NAME = 'chevah-weblibs-bootstrap-datepicker'
MODULE_NAME = 'bootstrap_datepicker'
VERSION = '1.2.0'
CHEVAH_VERSION = '+chevah.3'
WEBSITE = 'http://eternicode.github.com/bootstrap-datepicker/'
AUTHOR = 'Andrew Rowls'
LICENSE = 'Apache 2.0'

BASE_URL = (
    'https://raw.github.com/eternicode/bootstrap-datepicker/%(version)s/')
BASE_PATH = 'chevah/weblibs/%s/' % (MODULE_NAME)
FILES = [
    ('js/', 'bootstrap-datepicker.js'),
    ('css/', 'datepicker.css'),
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
for (remote_path, filename) in FILES:
    remote = (BASE_URL + remote_path + filename) % {'version': VERSION}
    local = add_version(BASE_PATH + filename)
    DOWNLOADS.append((remote, local))


context = ssl.create_default_context()
context.check_hostname = False
context.verify_mode = ssl.CERT_NONE


def download():
    """
    Download files.
    """
    import urllib2
    for remote, local in DOWNLOADS:
        print("Getting %s into %s" % (remote, local))
        mp3file = urllib2.urlopen(remote, context=context)
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

    def finalize_options(self):
        self.cwd = os.getcwd()

    def run(self):
        assert os.getcwd() == self.cwd, (
            'Must be in package root: %s' % self.cwd)
        download()
        self.run_command('bdist_wheel')

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
                '*.png',
                '*.gif',
                '*.jpg',
                ]})
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
    namespace_packages=['chevah', 'chevah.weblibs'],
    packages=['chevah', 'chevah.weblibs', 'chevah.weblibs.' + MODULE_NAME],
    package_data=find_package_data(['chevah.weblibs.' + MODULE_NAME]),
    cmdclass={
        'publish': PublishCommand,
        },
    )
