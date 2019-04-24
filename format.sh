#!/usr/bin/env bash
files=( "spotifycli/spotifycli.py" "spotifycli/version.py" "spotifycli/__main__.py" "spotifycli/__init__.py" "setup.py" )
for i in "${files[@]}"
do
    :
    autopep8 --in-place --aggressive $i
done
