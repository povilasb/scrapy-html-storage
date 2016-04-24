virtualenv_dir := pyenv
pip := $(virtualenv_dir)/bin/pip
pytest := $(virtualenv_dir)/bin/py.test
pylint := $(virtualenv_dir)/bin/pylint
coverage := $(virtualenv_dir)/bin/coverage


qa: lint test
.PHONY: qa

lint:
	$(pylint) scrapy_html_storage/
.PHONY: lint

test: $(virtualenv_dir)
	PYTHONPATH=$(PYTHONPATH):. $(coverage) run \
		--source scrapy_html_storage $(pytest) -s tests
	$(coverage) report -m
.PHONY: test

$(virtualenv_dir): requirements/dev.txt
	virtualenv $@
	$(pip) install -r $<
