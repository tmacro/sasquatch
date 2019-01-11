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
	$(REPORT) Building docker image $(DOCKER_IMAGE)
	$(ECHO) -n "   - Using tags: $(DEFAULT_DOCKER_TAG)"
ifdef DOCKER_TAG_VERSION
	$(ECHO) -n ", $(PKG_VERSION)"
endif
	$(ECHO)
	$(REPORT) Tagging docker images
	$(STEP) Tagging $(DOCKER_IMAGE):$(DEFAULT_DOCKER_TAG)
	$(V)docker build -t $(DOCKER_IMAGE):$(DEFAULT_DOCKER_TAG) . $(_REDIRECT)
ifdef DOCKER_TAG_VERSION
	$(STEP) Tagging $(DOCKER_IMAGE):$(PKG_VERSION)
	$(V)docker tag $(DOCKER_IMAGE):latest $(DOCKER_IMAGE):$(PKG_VERSION) $(_REDIRECT)
endif
.PHONY: build-docker

build: build-docker build-pypi
	$(REPORT) Finished Building $(PKG_NAME)-$(PKG_VERSION)
.PHONY: build

docker-login:
	echo "$(DOCKER_PASSWORD)" | docker login -u "$(DOCKER_USERNAME)" --password-stdin

release-docker: build-docker
ifdef DOCKER_LOGIN
	make -e docker-login
endif
	$(REPORT) Pushing images to $(DOCKER_IMAGE)
	$(STEP) Pushing $(DOCKER_IMAGE):$(DEFAULT_DOCKER_TAG)
	$(V)docker push $(DOCKER_IMAGE):$(DEFAULT_DOCKER_TAG) $(_REDIRECT)
ifdef DOCKER_TAG_VERSION
	$(STEP) Pushing $(DOCKER_IMAGE):$(PKG_VERSION)
	$(V)docker push $(DOCKER_IMAGE):$(PKG_VERSION) $(_REDIRECT)
endif
.PHONY: release-docker

release-pypi: build-pypi
	$(REPORT) Releasing $(PKG_NAME)-$(PKG_VERSION) to PyPi
	$(V)twine upload "dist/$(PKG_NAME)-$(PKG_VERSION).tar.gz"
.PHONY: release-pypi

release: release-docker release-pypi
.PHONY: release

test:
	pytest
