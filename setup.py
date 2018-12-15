from distutils.core import setup
from spotifycli.version import __version__

setup(
    name = 'spotify-cli-linux',
    version = __version__,
    description = 'A command-line interface to Spotify on Linux',
    author = 'pwittchen',
    author_email = 'piotr.wittchen@gmail.com',
    url = 'https://github.com/pwittchen/spotify-cli-linux',
    license = 'GPL 3.0',
    packages = ['spotifycli'],
    entry_points = {
       "console_scripts": ['spotifycli = spotifycli.spotifycli:main']
    },
)
