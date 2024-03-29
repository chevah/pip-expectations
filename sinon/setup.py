"""
Python packaging definition.

It downloads the JS and CSS Files from upstream website
and creates a package.
"""
from __future__ import print_function
from setuptools import setup, Command
import os
import ssl

NAME = 'chevah-weblibs-sinon'
VERSION = '1.5.2'
CHEVAH_VERSION = '+chevah.4'
DOWNLOADS = [
    ('http://sinonjs.org/releases/sinon-%(version)s.js',
        'chevah/weblibs/sinon/sinon.js'),
    ]


context = ssl.create_default_context()
context.check_hostname = False
context.verify_mode = ssl.CERT_NONE


def download():
    """
    Download file.
    """
    import urllib2
    for remote, local in DOWNLOADS:
        url = remote % {'version': VERSION}
        mp3file = urllib2.urlopen(url, context=context)
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
    author='Christian Johansen',
    maintainer="Adi Roiban",
    maintainer_email="adi.roiban@chevah.com",
    license='BSD',
    platforms='any',
    description='Files for Sinon used in Chevah project.',
    long_description=open('README.rst').read(),
    url='http://sinonjs.org/',
    namespace_packages=['chevah', 'chevah.weblibs'],
    packages=['chevah', 'chevah.weblibs', 'chevah.weblibs.sinon'],
    package_data=find_package_data(['chevah.weblibs.sinon']),
    cmdclass={
        'publish': PublishCommand,
        },
    )
