#
# To update this, manually download the wanted released from
# https://github.com/mtkennerly/shawl/releases
# Then copy the file as shawl.exe inside chevah/shawl
from setuptools import setup, Command

NAME = 'chevah-shawl'
MODULE_NAME = 'chevah_shawl'
VERSION = '1.5.0'
CHEVAH_VERSION = '+chevah.1'
WEBSITE = 'https://github.com/mtkennerly/shawl'
AUTHOR = 'Matthew T. Kennerly'
LICENSE = 'MIT'


setup(
    name=NAME,
    version=VERSION + CHEVAH_VERSION,
    author=AUTHOR,
    author_email='hidden',
    maintainer="Adi Roiban",
    maintainer_email="adi.roiban@chevah.com",
    license=LICENSE,
    platforms='any',
    description='Files for %s used in Chevah project.'.format(MODULE_NAME),
    long_description=open('README.rst').read(),
    url=WEBSITE,
    packages=[MODULE_NAME],
    package_dir={MODULE_NAME: MODULE_NAME},
    package_data={MODULE_NAME: ['*']},
    )
