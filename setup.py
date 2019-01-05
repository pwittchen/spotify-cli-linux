from setuptools import setup
from distutils.core import setup
from spotifycli.version import __version__
from spotifycli.spotifycli import __doc__

with open("README.md", "r") as readme_content:
    long_description = readme_content.read()

setup(
    name='spotify-cli-linux',
    version=__version__,
    description=__doc__,
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='pwittchen',
    author_email='piotr.wittchen@gmail.com',
    url='https://github.com/pwittchen/spotify-cli-linux',
    license='GPL 3.0',
    packages=['spotifycli'],
    entry_points={
        "console_scripts": ['spotifycli = spotifycli.spotifycli:main']
    },
)
