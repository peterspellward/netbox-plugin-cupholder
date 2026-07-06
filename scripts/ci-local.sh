#!/usr/bin/env bash
# Run the same checks as .github/workflows/ci.yaml before pushing.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
NETBOX_REF="${NETBOX_REF:-v4.5.10}"
NETBOX_DIR="${NETBOX_DIR:-$ROOT/.cache/netbox-${NETBOX_REF#v}}"
PYTHON="${PYTHON:-python3}"
RUFF_VERSION="${RUFF_VERSION:-0.11.12}"
CI_VENV="${CI_VENV:-$ROOT/.cache/ci-venv}"

ensure_ci_venv() {
  if [[ ! -x "$CI_VENV/bin/python" ]]; then
    mkdir -p "$(dirname "$CI_VENV")"
    "$PYTHON" -m venv "$CI_VENV"
    "$CI_VENV/bin/pip" install -q "ruff==${RUFF_VERSION}"
  fi
}

echo "==> Lint (ruff==${RUFF_VERSION}, matches CI)"
ensure_ci_venv
"$CI_VENV/bin/ruff" check "$ROOT/netbox_cup_holder_plugin/"

echo "==> Ensure NetBox ${NETBOX_REF} checkout at ${NETBOX_DIR}"
if [[ ! -f "$NETBOX_DIR/netbox/manage.py" ]]; then
  mkdir -p "$NETBOX_DIR"
  tmp="$(mktemp -d)"
  curl -sL "https://github.com/netbox-community/netbox/archive/refs/tags/${NETBOX_REF}.tar.gz" \
    | tar xz --strip-components=1 -C "$tmp"
  rm -rf "$NETBOX_DIR"
  mv "$tmp" "$NETBOX_DIR"
fi

echo "==> Validate migration dependencies against ${NETBOX_REF}"
"$PYTHON" "$ROOT/scripts/validate_migration_deps.py" "$NETBOX_DIR"

if [[ "${CI_LOCAL_SKIP_TESTS:-0}" == "1" ]]; then
  echo "==> Skipping integration tests (CI_LOCAL_SKIP_TESTS=1)"
  echo "All pre-push checks passed."
  exit 0
fi

echo "==> Install NetBox + plugin"
"$CI_VENV/bin/pip" install -q -r "$NETBOX_DIR/requirements.txt"
"$CI_VENV/bin/pip" install -q -e "$ROOT" --no-deps

NETBOX_MANAGE="$NETBOX_DIR/netbox/manage.py"
PLUGIN_CONFIG="$ROOT/testing/configuration.py"
export DB_HOST="${DB_HOST:-localhost}"
export DB_PORT="${DB_PORT:-5432}"
export DB_NAME="${DB_NAME:-netbox}"
export DB_USER="${DB_USER:-netbox}"
export DB_PASSWORD="${DB_PASSWORD:-netbox}"
export REDIS_HOST="${REDIS_HOST:-localhost}"
export REDIS_PORT="${REDIS_PORT:-6379}"

cp "$PLUGIN_CONFIG" "$NETBOX_DIR/netbox/netbox/configuration.py"

echo "==> Migrate (CI uses testing/configuration.py)"
"$CI_VENV/bin/python" "$NETBOX_MANAGE" migrate --no-input

echo "==> Check for missing migrations"
"$CI_VENV/bin/python" "$NETBOX_MANAGE" makemigrations --check netbox_cup_holder_plugin

echo "==> Run tests (CI configuration)"
"$CI_VENV/bin/python" "$NETBOX_MANAGE" test netbox_cup_holder_plugin.tests --parallel --keepdb -v 1

echo "All CI checks passed locally."
