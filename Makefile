include conf.make

ifndef VERBOSE
V = @
_REDIRECT = 1>/dev/null >&1
endif

ECHO = @echo
REPORT = $(ECHO) ::
STEP = $(ECHO) "   -"

VENV = .venv
VENV_ACTIVATE = $(VENV)/bin/activate

DOCKER_IMAGE = $(DOCKER_USER)/$(DOCKER_REPO)

default: build

VENV_CREATED = $(VENV)/.venv-created
$(VENV_CREATED):
	$(REPORT) "Creating virtual environment..."
	$(V)python -m venv .venv \
		&& source $(VENV_ACTIVATE) \
		&& pip install --upgrade pip $(_REDIRECT) \
		&& deactivate \
		touch $(VENV_CREATED)

DEPS_INSTALLED = $(VENV)/.deps-installed
$(DEPS_INSTALLED): $(VENV_CREATED)
	$(REPORT) "Installing dependencies..."
	$(V)source $(VENV_ACTIVATE) \
		&& pip install -r requirements.txt $(_REDIRECT)
	$(V)touch $(DEPS_INSTALLED)


develop: $(DEPS_INSTALLED)
	$(REPORT) "Enabling development mode..."
	$(V)source $(VENV_ACTIVATE) \
		&& python setup.py develop $(_REDIRECT)
.PHONY: develop

clean:
	$(V)find $(PKG_NAME) -name __pycache__ -exec rm -rf "{}" +
	$(V)rm -rf $(PKG_NAME).egg-info
.PHONY: clean

fclean: clean
	$(V)rm -rf dist/
	$(V)rm -rf $(VENV)
.PHONY: fclean

build-pypi:
	$(REPORT) Building python sdist...
	$(V)python setup.py sdist $(_REDIRECT)
.PHONY: build-pypi

build-docker:
	$(REPORT) Building docker images $(DOCKER_IMAGE)
	$(STEP) Using tags: latest, $(PKG_VERSION)
	$(V)docker build -t $(DOCKER_IMAGE) . $(_REDIRECT)
	$(STEP) Tagging $(DOCKER_IMAGE):$(PKG_VERSION)
	$(V)docker tag $(DOCKER_IMAGE):latest $(DOCKER_IMAGE):$(PKG_VERSION) $(_REDIRECT)
.PHONY: build-docker

build: build-docker build-pypi
	$(REPORT) Finished Building $(PKG_NAME)-$(PKG_VERSION)
.PHONY: build

release-docker: build-docker
	$(REPORT) Pushing images to $(DOCKER_IMAGE)
	$(STEP) Pushing $(DOCKER_IMAGE):latest
	$(V)docker push $(DOCKER_IMAGE):latest $(_REDIRECT)
	$(STEP) Pushing $(DOCKER_IMAGE):$(PKG_VERSION)
	$(V)docker push $(DOCKER_IMAGE):$(PKG_VERSION) $(_REDIRECT)
.PHONY: release-docker

release-pypi: build-pypi
	$(REPORT) Releasing $(PKG_NAME)-$(PKG_VERSION) to PyPi
	$(V)twine upload "dist/$(PKG_NAME)-$(PKG_VERSION).tar.gz
.PHONY: release-pypi

release: build release-docker release-pypi
.PHONY: release

test:
	pytest
