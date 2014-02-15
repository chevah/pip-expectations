"""
Python packaging definition for LessCSS files.

It downloads the minified file from LessCSS website and creates a package.
"""

from setuptools import setup, Command
import os

NAME = 'chevah-weblibs-less'
VERSION = '1.6.3'
CHEVAH_VERSION = '.c1'

DOWNLOADS = [
    ('https://raw.github.com/cloudhead/less.js/master/dist/'
            'less-%(version)s.min.js',
        'chevah/weblibs/lesscss/less.min.js'),
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
                'bin/*',
                'lib/less/*.js',
                'lib/less/tree/*.js',
                ]})
    return result


setup(
    name=NAME,
    version=VERSION + CHEVAH_VERSION,
    maintainer="Adi Roiban",
    maintainer_email="adi.roiban@chevah.com",
    license='Same as LessCSS',
    platforms='any',
    description='Files for LessCSS used in Chevah project.',
    long_description=open('README.rst').read(),
    url='http://lesscss.org/',
    namespace_packages=['chevah', 'chevah.weblibs'],
    packages=['chevah', 'chevah.weblibs', 'chevah.weblibs.lesscss'],
    package_data=find_package_data(['chevah.weblibs.lesscss']),
    cmdclass={
        'publish': PublishCommand,
        },
    )
