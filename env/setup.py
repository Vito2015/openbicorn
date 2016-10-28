#!/usr/bin/env python
# coding: utf-8
import codecs
from setuptools import setup, find_packages
import bicorn


def read_string(*fnames, **kwargs):
    buf = read_lines(*fnames, **kwargs)
    return ''.join(buf)


def read_lines(*fnames, **kwargs):
    encoding = kwargs.get('encoding', 'utf-8')
    buf = []
    for fname in fnames:
        buf.extend(codecs.open(fname, encoding=encoding).readlines())
    return buf


# class PyTest(TestCommand):
#     def finalize_options(self):
#         TestCommand.finalize_options(self)
#         self.test_args = []
#         self.test_suite = True
#
#     def run_tests(self):
#         import pytest
#         errcode = pytest.main(self.test_args)
#         sys.exit(errcode)


setup(
    name='bicorn',
    version=bicorn.__version__,
    # tests_require=['pytest'],
    # install_requires=read_lines('requirements.txt'),
    # install_requires=['pytest>=2.8.7'],
    description='thrift application with gunicorn and zookeeper',
    author='Vito',
    author_email='wangye@xiaomi.com',
    url='',
    download_url='',
    license='GNU',
    packages=find_packages(),
    package_data={'doc': ['*.txt'], 'xml': ['*.xml', 'relax/*.rnc']},
    # packages=['bicorn'],
    # scripts=['bicorn/scripts/bicorn'],
    entry_points={
        'console_scripts': [
            'bicorn = bicorn:thriftzoo_main',
            'gunthrift = bicorn:gunthrift_main',
        ]
    },
    keywords='thrift gunicorn zookeeper',
    long_description=read_string('README'),
    platforms='any',
    zip_safe=True,
    classifiers=['Development Status :: 4 - Beta',
                 'Intended Audience :: Developers',
                 'License :: OSI Approved :: GNU General Public License v2 or later (GPLv2+)',
                 'Operating System :: OS Independent',
                 'Programming Language :: Python',
                 'Topic :: Software Development :: Libraries',
                 ],

)