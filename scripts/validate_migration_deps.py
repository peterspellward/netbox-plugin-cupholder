#!/usr/bin/env python3
"""
Verify plugin migration dependencies exist in a NetBox checkout.

CI clones a specific NetBox release; if plugin migrations reference core
migrations that only exist on newer NetBox, the job fails with NodeNotFoundError.
Run this against the same NetBox ref as .github/workflows/ci.yaml before pushing.
"""

from __future__ import annotations

import ast
import sys
from pathlib import Path


def parse_dependencies(migration_file: Path) -> list[tuple[str, str]]:
    tree = ast.parse(migration_file.read_text())
    for node in tree.body:
        if not isinstance(node, ast.ClassDef) or node.name != 'Migration':
            continue
        for item in node.body:
            if not isinstance(item, ast.Assign):
                continue
            for target in item.targets:
                if isinstance(target, ast.Name) and target.id == 'dependencies':
                    return ast.literal_eval(item.value)
    return []


def netbox_migration_names(netbox_root: Path, app_label: str) -> set[str]:
    migrations_dir = netbox_root / 'netbox' / app_label / 'migrations'
    if not migrations_dir.is_dir():
        raise FileNotFoundError(f'No migrations directory for app {app_label!r} under {netbox_root}')
    return {
        path.stem
        for path in migrations_dir.glob('*.py')
        if path.name != '__init__.py'
    }


def main() -> int:
    repo_root = Path(__file__).resolve().parents[1]
    plugin_migrations = repo_root / 'netbox_cup_holder_plugin' / 'migrations'
    netbox_root = Path(
        sys.argv[1] if len(sys.argv) > 1 else repo_root / '.cache' / 'netbox-v4.5.10'
    ).resolve()

    if not netbox_root.is_dir():
        print(
            f'NetBox checkout not found at {netbox_root}\n'
            'Run: scripts/ci-local.sh (clones automatically) or set NETBOX_DIR',
            file=sys.stderr,
        )
        return 1

    errors: list[str] = []
    for migration_file in sorted(plugin_migrations.glob('0*.py')):
        for app_label, migration_name in parse_dependencies(migration_file):
            if app_label == 'netbox_cup_holder_plugin':
                continue
            try:
                available = netbox_migration_names(netbox_root, app_label)
            except FileNotFoundError as exc:
                errors.append(f'{migration_file.name}: {exc}')
                continue
            if migration_name not in available:
                errors.append(
                    f'{migration_file.name}: missing dependency '
                    f"({app_label!r}, {migration_name!r}) — not in NetBox at {netbox_root.name}"
                )

    if errors:
        print('Migration dependency check failed:', file=sys.stderr)
        for error in errors:
            print(f'  - {error}', file=sys.stderr)
        return 1

    print(f'Migration dependencies OK against {netbox_root}')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
