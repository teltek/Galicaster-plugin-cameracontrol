# Always prefer setuptools over distutils
from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='galicaster_plugin_cameracontrol',

    # Versions should comply with PEP440.  For a discussion on single-sourcing
    # the version across setup.py and the project code, see
    # https://packaging.python.org/en/latest/single_source_version.html
    version='1.0.1',

    description='Plugin to control remote cameras using Galicaster GUI',
    long_description=long_description,

    # The project's main homepage.
    url='https://github.com/teltek/Galicaster-plugin-cameracontrol',

    # Choose your license
    license='CC BY-NC-SA',


    # You can just specify the packages manually here if your project is
    # simple. Or you can use find_packages().
    packages=find_packages(exclude=['contrib', 'docs', 'tests']),

    # Use resources/*.* to copy only files, if use resources/* it will fail in some computers see TTK_15131
    include_package_data=True,
    package_data={"" : ["resources/*.*"]},

    # List run-time dependencies here.  These will be installed by pip when
    # your project is installed. For an analysis of "install_requires" vs pip's
    # requirements files see:
    # https://packaging.python.org/en/latest/requirements.html
    install_requires=['pyserial', 'requests'],
)
