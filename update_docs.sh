#!/usr/bin/env bash
git checkout gh-pages
git show master:README.md >README.md
git add -A
git commit -m "updating docs"
echo "docs updated, now you can push your changes"
