dist:
	sudo python setup.py sdist
upload:
	twine upload dist/*
release: clean
	sudo python setup.py sdist && twine upload dist/*
clean:
	sudo rm MANIFEST || true && sudo rm -rf dist/ || true && sudo rm -rf spotify_cli_linux.egg-info || true
format:
	autopep8 --in-place --aggressive spotifycli/spotifycli.py
check_format:
	pycodestyle spotifycli/spotifycli.py
docs:
	./update_docs.sh
