ve:
	python3 -m venv .ve; \
	. .ve/bin/activate; \
	pip install -r requirements.txt

clean:
	test -d .ve && rm -rf .ve

install_hooks:
	pip install -r requirements-ci.txt; \
	pre-commit install

run_jupyter:
	jupyter nbclassic

run_hooks:
	pre-commit run --all-files

style:
	flake8 main

types:
	mypy --namespace-packages -p "news" --config-file setup.cfg

format:
	black main --check

lint:
	flake8 main
	isort main --diff
	black main --check
	mypy --namespace-packages -p "news" --config-file setup.cfg
