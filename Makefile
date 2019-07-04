clean:
	sudo rm -rf dist/ || true && sudo rm -rf spotify_cli_linux.egg-info || true && sudo rm spotifycli/*.pyc || true && sudo rm -rf spotifycli/__pycache__ || true
dist:
	python3 setup.py sdist
upload:
	twine upload dist/*
release: clean dist upload
requirements:
	sudo pip install -r dev-requirements.txt --upgrade
format:
	./format.sh
checkformat:
	./checkformat.sh
lint:
	pylint spotifycli/spotifycli.py spotifycli/version.py spotifycli/__main__.py spotifycli/__init__.py setup.py
docs:
	./update_docs.sh
