MY_VAR := ${shell python -c 'from pony_up import __version__ as v; print(v)'}

clean:
	rm -rf *.so *.egg-info build *.png *.log *.svg

setup:
	pip install twine

upload: clean
	python setup.py sdist
	@echo UPLOADING VERSION $(MY_VAR)
	twine upload dist/pony_up-${MY_VAR}.tar.gz
