# -*- coding: utf-8 -*-

"""cactidbadapter setup.py."""

from setuptools import setup
from setuptools.command.test import test as TestCommand
import sys
import os


class Tox(TestCommand):

    """Tox."""

    user_options = [('tox-args=', 'a', "Arguments to pass to tox")]

    def initialize_options(self):
        """Iinit."""
        TestCommand.initialize_options(self)
        self.tox_args = None

    def finalize_options(self):
        """Finalize."""
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        """Run."""
        import tox
        import shlex
        if self.tox_args:
            errno = tox.cmdline(args=shlex.split(self.tox_args))
        else:
            errno = tox.cmdline(self.tox_args)
        sys.exit(errno)


classifiers = [
    "Development Status :: 3 - Alpha",
    "Programming Language :: Python",
    "Programming Language :: Python :: 2",
    "Programming Language :: Python :: 2.7",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.4",
    "Programming Language :: Python :: Implementation :: CPython",
    "Programming Language :: Python :: Implementation :: PyPy",
]

here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'README.rst')) as _file:
    README = _file.read()

requires = ['PyMySQL']

with open('requirements.txt', 'w') as _file:
    _file.write('\n'.join(requires))

setup(
    name="cactidbadapter",
    version="0.1.2",
    description='CactiDB Adapter.',
    long_description=README,
    author='Toshikatsu Murakoshi',
    author_email='mtoshi.g@gmail.com',
    url='https://github.com/mtoshi/cactidbadapter',
    license='MIT',
    classifiers=classifiers,
    py_modules=['cactidbadapter'],
    data_files=[],
    install_requires=requires,
    include_package_data=True,
    tests_require=['tox'],
    cmdclass={'test': Tox},
)
