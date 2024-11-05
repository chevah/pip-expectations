#
# To update this, manually download the wanted released from
# https://github.com/vercel/geist-font/ and copy them inside chevah_geist
# directory.
from setuptools import setup, Command

NAME = 'chevah-geist'
MODULE_NAME = 'chevah_geist'
VERSION = '1.4.1'
CHEVAH_VERSION = '+chevah.2'
WEBSITE = 'https://github.com/vercel/geist-font/'
AUTHOR = 'Vercel'
LICENSE = 'OFL-1.1'


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
