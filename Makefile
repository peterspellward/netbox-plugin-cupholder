sources = netbox_cup_holder_plugin
NETBOX_REF ?= v4.5.10
NETBOX_DIR ?= .cache/netbox-$(NETBOX_REF:v%=%)
RUFF_VERSION ?= 0.11.12
PYTHON ?= python3

.PHONY: test format lint unittest pre-commit clean ci ci-quick check-migration-deps install-pre-push-hook

test: format lint unittest

format:
	ruff check --select I --fix $(sources) tests
	ruff format $(sources) tests

lint:
	$(PYTHON) -m pip install -q ruff==$(RUFF_VERSION)
	$(PYTHON) -m ruff check $(sources)

check-migration-deps:
	@test -d "$(NETBOX_DIR)" || $(MAKE) fetch-netbox
	$(PYTHON) scripts/validate_migration_deps.py "$(NETBOX_DIR)"

fetch-netbox:
	@mkdir -p .cache
	@rm -rf "$(NETBOX_DIR)"
	@mkdir -p "$(NETBOX_DIR)"
	@curl -sL "https://github.com/netbox-community/netbox/archive/refs/tags/$(NETBOX_REF).tar.gz" \
		| tar xz --strip-components=1 -C "$(NETBOX_DIR)"

# Mirror GitHub Actions (requires PostgreSQL + Redis on localhost)
ci:
	./scripts/ci-local.sh

# Lint + migration graph only — fast pre-push smoke test
ci-quick:
	CI_LOCAL_SKIP_TESTS=1 ./scripts/ci-local.sh

install-pre-push-hook:
	cp .hooks/pre-push .git/hooks/pre-push
	chmod +x .git/hooks/pre-push
	@echo "Installed pre-push hook (runs: make ci-quick)"

pre-commit:
	pre-commit run --all-files

unittest:
	@echo "Run from NetBox: NETBOX_CONFIGURATION=netbox_cup_holder_plugin.test_configuration python manage.py test netbox_cup_holder_plugin.tests"
	@echo "Or: make ci"

clean:
	rm -rf *.egg-info
	rm -rf .tox dist site .cache
