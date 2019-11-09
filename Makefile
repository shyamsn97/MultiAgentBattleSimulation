lint:
	isort -y
	black .
	flake8 .

push:
	make lint
	git add .
	git commit
	git push origin HEAD

install:
	make lint
	python setup.py install