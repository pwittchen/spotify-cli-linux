dist:
	python setup.py sdist
release:
	twine upload dist/*
clean:
	rm MANIFEST && rm -rf dist/
