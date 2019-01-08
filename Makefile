dist:
	sudo python setup.py sdist
upload:
	twine upload dist/*
release: clean dist upload
clean:
	sudo rm MANIFEST || true && sudo rm -rf dist/ || true && sudo rm -rf spotify_cli_linux.egg-info || true
format:
	autopep8 --in-place --aggressive spotifycli/spotifycli.py	
	autopep8 --in-place --aggressive spotifycli/version.py
	autopep8 --in-place --aggressive spotifycli/__main__.py
	autopep8 --in-place --aggressive spotifycli/__init__.py
	autopep8 --in-place --aggressive setup.py
check:
	pycodestyle --show-source --show-pep8 --format=default spotifycli/spotifycli.py	
	pycodestyle --show-source --show-pep8 --format=default spotifycli/version.py
	pycodestyle --show-source --show-pep8 --format=default spotifycli/__main__.py
	pycodestyle --show-source --show-pep8 --format=default spotifycli/__init__.py
	pycodestyle --show-source --show-pep8 --format=default setup.py
docs:
	./update_docs.sh
