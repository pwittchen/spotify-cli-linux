from setuptools import setup
from distutils.core import setup
from spotifycli.version import __version__
from spotifycli.spotifycli import __doc__

setup(
    name='spotify-cli-linux',
    version=__version__,
    python_requires='>=3.6',
    description=__doc__,
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    author='Piotr Wittchen',
    author_email='piotr.wittchen@gmail.com',
    url='https://github.com/pwittchen/spotify-cli-linux',
    license='GPL 3.0',
    packages=['spotifycli'],
    install_requires=['lyricwikia'],
    entry_points={
        "console_scripts": ['spotifycli = spotifycli.spotifycli:main']
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Multimedia :: Sound/Audio'
    ],
)
