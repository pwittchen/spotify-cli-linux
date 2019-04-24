#!/usr/bin/env bash
files=( "spotifycli/spotifycli.py" "spotifycli/version.py" "spotifycli/__main__.py" "spotifycli/__init__.py" "setup.py" )
for i in "${files[@]}"
do
    :
    pycodestyle --show-source --show-pep8 --format=default $i
done
