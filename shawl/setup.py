#
# To update this, manually download the wanted released from
# https://github.com/mtkennerly/shawl/releases
# Then copy the file as shawl.exe inside chevah/shawl
from setuptools import setup, Command
import os

NAME = 'chevah-shawl'
MODULE_NAME = 'shawl'
VERSION = '1.2.0'
CHEVAH_VERSION = '+chevah.1'
WEBSITE = 'https://github.com/mtkennerly/shawl'
AUTHOR = 'Matthew T. Kennerly'
LICENSE = 'MIT'


def find_package_data(modules):
    """
    Returns the static dictionary of data files.
    """
    result = {}
    for module in modules:
        result.update({
            module: ['*.exe']})
    return result

package_name = 'chevah.' + MODULE_NAME


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
    packages=['chevah', package_name],
    package_dir={package_name: 'chevah/' + MODULE_NAME},
    package_data={package_name: ['*']},
    )
