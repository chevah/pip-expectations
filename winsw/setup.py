from setuptools import setup, Command
import os

NAME = 'chevah-winsw'
MODULE_NAME = 'winsw'
VERSION = '2.5.0'
CHEVAH_VERSION = '.chevah3'
WEBSITE = 'https://github.com/winsw/winsw/'
AUTHOR = 'WinSw Team'
LICENSE = 'MIT'

BASE_URL = (
    # Upstream
    'https://github.com/winsw/winsw/releases/download/v%(version)s/WinSW.NETCore31.x86.exe'
    )

remote = BASE_URL % {'version': VERSION}
local = 'build/sftpplus-service-manager.exe'


def download():
    """
    Download files.
    """
    import urllib2
    print("Getting %s into %s" % (remote, local))
    stream = urllib2.urlopen(remote)
    output = open(local, 'wb')
    output.write(stream.read())
    output.close()


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
        download()
        self.run_command('bdist_wheel')

        # Upload package to Chevah PyPi server.
        upload_command = self.distribution.get_command_obj('upload')
        upload_command.repository = u'chevah'
        self.run_command('upload')

        # Delete temporary files downloaded only for building the package.
        os.remove(local)


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
