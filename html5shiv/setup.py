"""
Python packaging definition.

It downloads the JS and CSS Files from upstream website
and creates a package.
"""

from setuptools import setup, Command
import os

NAME = 'chevah-weblibs-html5shiv'
VERSION = '3.7.0'
CHEVAH_VERSION = '.c1'
DOWNLOADS = [
    ('https://raw.github.com/aFarkas/html5shiv/%(version)s/dist/html5shiv.js',
        'chevah/weblibs/html5shiv/html5shiv.min.js'),
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


def download():
    """
    Download file.
    """
    import urllib2
    for remote, local in DOWNLOADS:
        url = remote % {'version': VERSION}
        mp3file = urllib2.urlopen(url)
        local = add_version(local)
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
            local = add_version(local)
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
    author='html5shiv Team',
    maintainer="Adi Roiban",
    maintainer_email="adi.roiban@chevah.com",
    license='MIT',
    platforms='any',
    description='Files for html5shiv used in Chevah project.',
    long_description=open('README.rst').read(),
    url='https://github.com/aFarkas/html5shiv',
    namespace_packages=['chevah', 'chevah.weblibs'],
    packages=['chevah', 'chevah.weblibs', 'chevah.weblibs.html5shiv'],
    package_data=find_package_data(['chevah.weblibs.html5shiv']),
    cmdclass={
        'publish': PublishCommand,
        },
    )
