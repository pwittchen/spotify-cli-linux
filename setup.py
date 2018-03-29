from distutils.core import setup

setup(
    name = 'spotify-cli-linux',
    version = '0.0.1',
    description = 'A command-line interface to Spotify on Linux',
    author = 'pwittchen',
    author_email = 'piotr.wittchen@gmail.com',
    url = 'https://github.com/pwittchen/spotify-cli-linux',
    py_modules=['spotify-cli-linux'],
    install_requires=[
        # list of this package dependencies
        # nothing right now
    ],
    entry_points='''
        [console_scripts]
        spotifycli=spotifycli:cli
    ''',
)
