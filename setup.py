import os
from setuptools import setup, find_packages

from flag_slurper import __version__

ROOT = os.path.dirname(__file__)


def read(fname):
    return open(os.path.join(ROOT, fname)).read()


setup(
    name='flag_slurper',
    version=__version__,
    description='Tool for getting flags from CDC machines',
    long_description=read('README.md'),
    author='Matt Gerst',
    author_email='mattgerst@gmail.com',
    license='MIT',
    packages=find_packages(),

    setup_requires=[
        'pytest-runner',
    ],
    install_requires=[
        'requests',
        'click',
    ],
    tests_require=[
        'pytest',
        'pytest-sugar',
        'tox',
    ],
    extras_require={
        'remote': [
            'paramiko',
        ],
    },

    classifiers=[
        'Development Status :: 1 - Planning',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'License :: OSI Approved :: MIT License',
    ],

    entry_points={
        'console_scripts': [
            'flag-slurper=flag_slurper.cli:cli',
        ]
    },
    package_data={
        'flag_bearer': ['default.ini'],
    },
)