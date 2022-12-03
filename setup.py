import setuptools

NAME = 'delineating'
VERSION = '1.0.0'
DESCRIPTION = 'Part of the contrasts project'
AUTHOR = 'greyhypotheses'
URL = 'https://github.com/plausibilities/delineating'
PYTHON_REQUIRES = '>=3.8'

with open('README.md') as f:
    readme = f.read()

setuptools.setup() (
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=readme,
    author=AUTHOR,
    url=URL,
    python_requires=PYTHON_REQUIRES,
    packages=setuptools.find_packages(exclude=['docs', 'tests'])
)