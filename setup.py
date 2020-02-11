# publish on pypi
# ---------------
#   $ python3 setup.py sdist bdist_wheel
#   $ twine upload --repository-url https://test.pypi.org/legacy/ dist/*
#   $ twine upload dist/*

import os
from setuptools import setup, find_packages


here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'README.md')) as fd:
    long_description = fd.read()


setup(
    name='docwatch',
    version='0.0.0',
    description='watch and convert a source document with pandoc',
    long_description=long_description,
    url='https://github.com/elcorto/docwatch',
    author='Steve Schmerler',
    author_email='git@elcorto.com',
    license='BSD 3-Clause',
    keywords='pandoc preview',
    package_dir={'': 'src'},
    packages=find_packages(where='src'),
    entry_points={
        'console_scripts': [
            'docwatch=docwatch.main:main',
        ],
    },
)
