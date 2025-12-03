from setuptools import setup
from distutils.core import setup
from spotifycli.version import __version__

setup(
    name='spotify_cli_linux',
    version=__version__,
    python_requires='>=3.12.7',
    description="a command line interface to Spotify on Linux",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    author='Piotr Wittchen',
    author_email='piotr.wittchen@gmail.com',
    url='https://github.com/pwittchen/spotify-cli-linux',
    license='GPL 3.0',
    packages=['spotifycli'],
    install_requires=['jeepney', 'lyricwikia'],
    entry_points={
        "console_scripts": ['spotifycli = spotifycli.spotifycli:main']
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python',
        'Topic :: Multimedia :: Sound/Audio'
    ],
)
