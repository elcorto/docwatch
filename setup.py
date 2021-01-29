import os
from setuptools import setup, find_packages


here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'README.md')) as fd:
    long_description = fd.read()


setup(
    name='docwatch',
    version='0.0.0',
    description='Convert, preview, watch and rebuild a source document with pandoc',
    long_description=long_description,
    url='https://github.com/elcorto/docwatch',
    author='Steve Schmerler',
    author_email='git@elcorto.com',
    python_requires='>=3.8',
    license='BSD 3-Clause',
    keywords='pandoc preview markdown latex pdf',
    package_dir={'': 'src'},
    packages=find_packages(where='src'),
    entry_points={
        'console_scripts': [
            'docwatch=docwatch.main:main',
        ],
    },
)
