from distutils.core import setup

setup(
    name = 'spotify-cli-linux',
    version = '0.0.3',
    description = 'A command-line interface to Spotify on Linux',
    author = 'pwittchen',
    author_email = 'piotr.wittchen@gmail.com',
    url = 'https://github.com/pwittchen/spotify-cli-linux',
    license = 'Apache 2.0',
    packages = ['spotifycli'],
    entry_points = {
       "console_scripts": ['spotifycli = spotifycli.spotifycli:main']
    },
)
