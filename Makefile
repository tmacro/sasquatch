
ifndef VERBOSE
V = @
_REDIRECT = 1>/dev/null >&1
endif


PKG_NAME = sasquatch

ECHO = @echo

VENV = .venv
VENV_ACTIVATE = $(VENV)/bin/activate



create-venv:
	$(ECHO) "Creating virtual environment..."
	$(V)python -m venv .venv \
		&& source $(VENV_ACTIVATE) \
		&& pip install --upgrade pip $(_REDIRECT)

VENV_CREATED = $(VENV)/.venv-created
$(VENV_CREATED): create-venv
	$(V)touch $(VENV_CREATED)

install-deps:
	$(ECHO) "Installing dependencies..."
	$(V)source $(VENV_ACTIVATE) \
		&& pip install -r requirements.txt $(_REDIRECT)

DEPS_INSTALLED = $(VENV)/.deps-installed
$(DEPS_INSTALLED): $(VENV_CREATED) install-deps
	$(V)touch $(DEPS_INSTALLED)


develop: $(DEPS_INSTALLED)
	$(ECHO) "Enabling development mode..."
	$(V)source $(VENV_ACTIVATE) \
		&& python setup.py develop $(_REDIRECT)

clean:
	$(V)find $(PKG_NAME) -name __pycache__ -exec rm -rf "{}" +
	$(V)rm -rf $(PKG_NAME).egg-info

fclean: clean
	$(V)rm -rf dist/
	$(V)rm -rf $(VENV)
