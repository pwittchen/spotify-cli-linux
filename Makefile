dist:
	sudo python setup.py sdist
upload:
	twine upload dist/*
release:
	sudo rm MANIFEST || true && sudo rm -rf dist/ || true && sudo python setup.py sdist && twine upload dist/*
clean:
	sudo rm MANIFEST || true && sudo rm -rf dist/ || true
format:
	autopep8 --in-place --aggressive spotifycli/spotifycli.py
check_format:
	pycodestyle spotifycli/spotifycli.py
docs:
	./update_docs.sh
