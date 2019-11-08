lint:
	isort -y
	black .
	# pep8ify .
	flake8 .

push:
	make lint
	git add .
	git commit
	git push origin HEAD

install:
	make lint
	python setup.py install