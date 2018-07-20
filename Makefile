dist:
	python setup.py sdist
release:
	twine upload dist/*
clean:
	rm MANIFEST && rm -rf dist/
format:
	autopep8 --in-place --aggressive spotifycli/spotifycli.py
check_format:
	pycodestyle spotifycli/spotifycli.py
