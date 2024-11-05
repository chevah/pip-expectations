from setuptools import setup, Command
import os
import ssl

NAME = 'chevah-rapidoc'
MODULE_NAME = 'chevah_rapidoc'
VERSION = '9.3.8'
CHEVAH_VERSION = '+chevah.2'
WEBSITE = 'https://github.com/rapi-doc/RapiDoc'
AUTHOR = 'RapiDoc Team'
LICENSE = 'MIT'

BASE_URL = (
    'https://raw.githubusercontent.com/rapi-doc/RapiDoc/refs/tags/v%(version)s/dist/'
    )
FILES = [
    ('', 'rapidoc-min.js'),
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
    local = add_version(MODULE_NAME + '/' + filename)
    DOWNLOADS.append((remote, local))

context = ssl.create_default_context()
context.check_hostname = False
context.verify_mode = ssl.CERT_NONE


def download():
    """
    Download files.
    """
    import urllib.request
    for remote, local in DOWNLOADS:
        print("Getting %s into %s" % (remote, local))
        mp3file = urllib.request.urlopen(remote, context=context)
        output = open(local, 'wb')
        output.write(mp3file.read())
        output.close()


class WheelCommand(Command):
    """
    Generate the Python wheel file
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

        # # Delete temporary files downloaded only for building the package.
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
    packages=[MODULE_NAME],
    package_data=find_package_data([MODULE_NAME]),
    cmdclass={
        'wheel': WheelCommand,
        },
    )
