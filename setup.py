import os
from setuptools import setup, find_packages

# Setup flags and parameters; pass in other arguments directly to setup() below
pkg_name = 'pensieve'  # top-level package name
scripts_dir = None  # if you have any useful executable scripts, specify their directory here, e.g. os.path.join(pkg_name, 'tools')
do_install_scripts = False  # enable this to install scripts in /usr/[local/]bin/ (this can be annoying unless installing in a virtualenv)

# Look for specific required packages here that are not registered with PyPI (and hence cannot be specified as dependencies)
try:
  import cv2
  print "setup.py: [INFO] OpenCV found; version: {}".format(cv2.__version__)
except ImportError:
  print "setup.py: [WARNING] OpenCV library not found; please install from: http://opencv.org/"

# Cache readme contents for use as long_description
readme = open('README.md').read()

# Find executable scripts to be installed, if desired
scripts = []
if do_install_scripts and scripts_dir is not None and os.path.isdir(scripts_dir):
  scripts = [os.path.join(scripts_dir, script) for script in os.listdir(scripts_dir) if script.endswith('.py') and not script == '__init__.py']
  print "setup.py: [INFO] Scripts to be installed: {}".format(", ".join(scripts))

# Call setup()
setup(
  name=pkg_name,
  version='0.1',
  description='An easy extensible server architecture to accept socket data such as sensor readings, images, etc.',
  long_description=readme,
  url='https://github.com/sinabahram/pensieve',
  author='Sina Bahram',
  author_email='sina@sinabahram.com',
  license='Mozilla Public License, version 2.0',
  packages=find_packages(),
  scripts=scripts,
  include_package_data=True,
  package_data={
    # Non-code files/wildcard-patterns to be installed with each package, specified as a dict with the package name as key
    pkg_name: [
      '*.yaml'
    ]
  },
  zip_safe=True,  # True if it is okay to zip up this package hierarchy for redistribution; False if, e.g. it writes temp/output files within this hierarchy, etc.
  install_requires=[
    'numpy',
    'pyzmq'
  ],
  test_suite=(pkg_name + '.tests'),  # test package names specified here are executed when you run: python setup.py test
  platforms='any',
  keywords='server utilities tools',  # add useful keywords here; if put up on PyPI, this facilitates better search
  classifiers=[
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 2.7',
    'Operating System :: OS Independent',
    'Topic :: Software Development :: Libraries :: Python Modules',
    'Topic :: Utilities'
  ])
