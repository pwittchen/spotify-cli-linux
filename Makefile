dist:
	sudo python setup.py sdist
upload:
	twine upload dist/*
release:
	sudo rm MANIFEST || true && sudo rm -rf dist/ || true && sudo python setup.py sdist && twine upload dist/*
clean:
	sudo rm MANIFEST && sudo rm -rf dist/
format:
	autopep8 --in-place --aggressive spotifycli/spotifycli.py
check_format:
	pycodestyle spotifycli/spotifycli.py
