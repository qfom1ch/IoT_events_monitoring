# Makefile

# --- CONFIG ---
DC_TEST = docker-compose -f docker-compose.test.yaml --env-file=.env.test
DC_DEV  = docker-compose -f docker-compose.dev.yaml --env-file=.env

# --- TEST ENV ---
.PHONY: test-up test-down test-pytest test-integration

test-up:
	$(DC_TEST) up -d

test-down:
	$(DC_TEST) down -v

test-run:
	uv run pytest -s

test-functional-run:
	uv run pytest -s tests/functional

test-integration-run:
	uv run pytest -s tests/integration

test-unit-run:
	uv run pytest -s tests/unit


# --- DEV ENV ---
.PHONY: dev-up dev-down

dev-up:
	$(DC_DEV) up -d

dev-down:
	$(DC_DEV) down



