from distutils.core import setup
from spotifycli.version import __version__
from spotifycli.spotifycli import __doc__

setup(
    name = 'spotify-cli-linux',
    version = __version__,
    description = __doc__,
    author = 'pwittchen',
    author_email = 'piotr.wittchen@gmail.com',
    url = 'https://github.com/pwittchen/spotify-cli-linux',
    license = 'GPL 3.0',
    packages = ['spotifycli'],
    entry_points = {
       "console_scripts": ['spotifycli = spotifycli.spotifycli:main']
    },
)
