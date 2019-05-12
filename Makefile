clean:
	sudo rm MANIFEST || true && sudo rm -rf dist/ || true && sudo rm -rf spotify_cli_linux.egg-info || true
dist:
	sudo python3 setup.py sdist
upload:
	twine upload dist/*
release: clean dist upload
requirements:
	pip install -r dev-requirements.txt --upgrade
format:
	./format.sh
checkformat:
	./checkformat.sh
lint:
	pylint spotifycli/spotifycli.py spotifycli/version.py spotifycli/__main__.py spotifycli/__init__.py setup.py
docs:
	./update_docs.sh
