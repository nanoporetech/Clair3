import os
import sys
import shutil
import re
import shutil
import platform
from glob import glob
from setuptools import setup, find_packages, Extension
from setuptools import Distribution, Command
from setuptools.command.install import install
import pkg_resources


#TODO: fill in these
__pkg_name__ = 'clair3'
__author__ = ''
__description__ = 'Clair3 - Integrating pileup and full-alignment for high-performance long-read variant calling'

# Use readme as long description and say its github-flavour markdown
from os import path
this_directory = path.abspath(path.dirname(__file__))
kwargs = {'encoding':'utf-8'} if sys.version_info.major == 3 else {}
with open(path.join(this_directory, 'README.md'), **kwargs) as f:
    __long_description__ = f.read()
__long_description_content_type__ = 'text/markdown'

__path__ = os.path.dirname(__file__)
__pkg_path__ = os.path.join(os.path.join(__path__, __pkg_name__))

# Get the version number from __init__.py
verstrline = open(os.path.join(__pkg_name__, '__init__.py'), 'r').read()
vsre = r"^__version__ = ['\"]([^'\"]*)['\"]"
mo = re.search(vsre, verstrline, re.M)
if mo:
    __version__ = mo.group(1)
else:
    raise RuntimeError('Unable to find version string in "{}/__init__.py".'.format(__pkg_name__))

dir_path = os.path.dirname(__file__)
with open(os.path.join(dir_path, 'requirements.txt')) as fh:
    install_requires = [
        str(requirement) for requirement in
        pkg_resources.parse_requirements(fh)]

data_files = []
extra_requires = {}
extensions = []

cwd = os.path.dirname(__file__)
src_dir = os.path.join(cwd, 'realign')

extensions.append(Extension(
    'clair3_realigner',
    include_dirs=[src_dir],
    sources=[
        os.path.join(src_dir, x)
        for x in ('ssw_cpp.cpp', 'ssw.c', 'realigner.cpp')],
    extra_compile_args=['-std=c++14', '-O1']))

# TODO: compiling this needs libboost-graph
#       the conda package doesn't appear to build
#       these extensions in any case
#extensions.append(Extension(
#    'clair3_debruijn_graph',
#    include_dirs=[src_dir],
#    sources=[
#        os.path.join(src_dir, x)
#        for x in ('debruijn_graph.cpp', )],
#    extra_compile_args=['-std=c++11', '-O3']))


setup(
    name=__pkg_name__,
    version=__version__,
    url='https://github.com/HKU-BAL/{}'.format(__pkg_name__),
    author=__author__,
    description=__description__,
    long_description=__long_description__,
    long_description_content_type=__long_description_content_type__,
    ext_modules=extensions,
    install_requires=install_requires,
    tests_require=[].extend(install_requires),
    # don't include any testing subpackages in dist
    packages=find_packages(exclude=['*.test', '*.test.*', 'test.*', 'test']),
    package_data={__pkg_name__:[os.path.join('data', '*')]},
    zip_safe=False,
    entry_points={
        'console_scripts': [
            '{0} = {0}:cli'.format(__pkg_name__)
        ]
    },
    scripts=[
        'scripts/clair3_hifi_quick_demo.sh',
        'scripts/clair3_ilmn_quick_demo.sh',
        'scripts/clair3_ont_quick_demo.sh',
        'scripts/clair3.sh',
        'scripts/run_clair3.sh']
)
