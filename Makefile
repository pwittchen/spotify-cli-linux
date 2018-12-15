dist:
	sudo python setup.py sdist
upload:
	twine upload dist/*
release:
	rm MANIFEST && rm -rf dist/ && sudo python setup.py sdist && twine upload dist/*
clean:
	rm MANIFEST && rm -rf dist/
format:
	autopep8 --in-place --aggressive spotifycli/spotifycli.py
check_format:
	pycodestyle spotifycli/spotifycli.py
