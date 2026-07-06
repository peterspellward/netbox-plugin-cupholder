# NetBox Cup Holder Plugin

Track rack-mounted cup holders in NetBox — because if you document every patch panel, you can document the thing keeping your overnight maintenance coffee off the floor.

* Free software: [Apache-2.0](LICENSE)
* Documentation: https://peterspellward.github.io/netbox-cup-holder-plugin/

## Overview

Data centre work runs on caffeine, and caffeine needs a home. This plugin extends NetBox to model **cup holders installed on racks**: what type they are, which rack they belong to, and which face they mount on.

It follows the same patterns as core NetBox DCIM objects:

| NetBox concept | Plugin equivalent |
|----------------|-------------------|
| Device Type | **Cup Holder Type** — catalog entry (size, material, description) |
| Device | **Cup Holder** — installed instance on a specific rack |

The plugin is a practical reference implementation for NetBox plugin development (models, UI, API, GraphQL, permissions, search, rack template extensions) with a memorable domain.

## Use cases

- **Operational visibility** — see at a glance which racks have a cup holder and where it is mounted.
- **Standardisation** — maintain a catalog of approved cup holder types rather than ad-hoc notes in rack comments.
- **Change tracking** — additions, moves, and replacements are journaled like any other NetBox object.
- **Automation** — query or update cup holders via REST API or GraphQL alongside your other infrastructure data.

## How it works

Each **cup holder type** describes a single-vessel design (one cup, mug, or flask). Types are seeded on install with twelve entries ranging from *Italiano Decadence* (XS, hand-carved teak) to *Weekend Warrior* (XXL, vacuum stainless).

Each **cup holder** is an installed instance with:

- A **name** (unique identifier)
- A **type** (required FK to the catalog)
- A **rack** (required — exactly **one cup holder per rack**)
- A **mount face**: front, left side, or right side (rear mounting is not supported)

Installed cup holders appear on the rack detail page. Types and instances each have their own list, filter, and detail views under the plugin menu.

```
Cup Holder Types (catalog)          Cup Holders (installed)
─────────────────────────          ───────────────────────
Big Joe 6000          ───────────►  CH-001  on Rack A42 (front)
Weekend Warrior                    CH-002  on Rack B07 (left)
…                                  …
```

## Features

- **Cup Holder Type catalog** — CRUD for types with size (XS–XXL), material, description, tags, and custom fields
- **Cup Holder instances** — assign a type to a rack with mount-face selection
- **One cup holder per rack** — enforced at the database level (`OneToOneField`)
- **Rack integration** — cup holder panel on the rack detail page
- **REST API** — full CRUD for types and instances
- **GraphQL** — query `cupholder`, `cupholder_list`, `cupholder_type`, and `cupholder_type_list`
- **NetBox-native behaviour** — change logging, journaling, permissions, global search, filtering, and bulk operations

## Typical workflow

1. **Review the type catalog** under *Plugins → Cup Holder Types*. The migration seeds twelve types; add or edit as needed.
2. **Create a cup holder** under *Plugins → Cup Holders*, selecting the rack, type, and mount face.
3. **Verify on the rack** — open the rack in DCIM; the cup holder panel shows the assigned instance.
4. **Automate** — use the API or GraphQL to report on racks missing a cup holder, or to bulk-update after a refresh project.

## Screenshots

_Screenshots will be added in a future release._

## Compatibility

This plugin requires **NetBox 4.5** or later.

| NetBox Version | Plugin Version |
|----------------|----------------|
| 4.5+           | 0.1.0          |

See [COMPATIBILITY.md](COMPATIBILITY.md) for details.

## Dependencies

- NetBox 4.5+
- Python 3.12+

No additional Python packages are required beyond NetBox's core dependencies.

## Installing

For NetBox Docker, see [Using NetBox Plugins with netbox-docker](https://github.com/netbox-community/netbox-docker/wiki/Using-Netbox-Plugins).

While the plugin is not yet published to PyPI, install from GitHub:

```bash
pip install git+https://github.com/peterspellward/netbox-cup-holder-plugin
```

Or add to `local_requirements.txt` / `plugin_requirements.txt` (netbox-docker):

```
git+https://github.com/peterspellward/netbox-cup-holder-plugin
```

Enable the plugin in `/opt/netbox/netbox/netbox/configuration.py`, or in netbox-docker's `/configuration/plugins.py`:

```python
PLUGINS = [
    'netbox_cup_holder_plugin',
]

PLUGINS_CONFIG = {
    'netbox_cup_holder_plugin': {},
}
```

Run migrations:

```bash
python manage.py migrate netbox_cup_holder_plugin
```

If upgrading from an earlier development build that used the old `CupholderModel` migrations, reset the app first:

```bash
python manage.py migrate netbox_cup_holder_plugin zero
python manage.py migrate netbox_cup_holder_plugin
```

## Configuration

No plugin-specific configuration is required. Optional settings can be added under `PLUGINS_CONFIG['netbox_cup_holder_plugin']` as the plugin evolves.

## REST API

| Endpoint | Description |
|----------|-------------|
| `/api/plugins/netbox_cup_holder_plugin/cup-holders/` | Installed cup holders |
| `/api/plugins/netbox_cup_holder_plugin/cup-holder-types/` | Type catalog |

Filter cup holders by rack, site, mount face, type, size, or material. See the [NetBox API documentation](https://docs.netbox.dev/en/stable/integrations/rest-api/) for authentication and pagination.

## GraphQL

The plugin registers queries for both catalog and instance objects:

- `cupholder` / `cupholder_list`
- `cupholder_type` / `cupholder_type_list`

GraphQL must be enabled in NetBox (`GRAPHQL_ENABLED = True`).

## Development

See [TESTING.md](TESTING.md) for running the test suite and [CONTRIBUTING.md](CONTRIBUTING.md) for contribution guidelines.

```bash
cd /path/to/netbox/netbox
NETBOX_CONFIGURATION=netbox_cup_holder_plugin.test_configuration \
  python manage.py test netbox_cup_holder_plugin.tests
```

## Contributing

Contributions are welcome. Please open issues or pull requests on [GitHub](https://github.com/peterspellward/netbox-cup-holder-plugin).

When reporting bugs, include NetBox version, plugin version, Python version, and steps to reproduce.

## Support

- **Documentation**: https://peterspellward.github.io/netbox-cup-holder-plugin/
- **Issues**: https://github.com/peterspellward/netbox-cup-holder-plugin/issues
- **Discussions**: https://github.com/peterspellward/netbox-cup-holder-plugin/discussions
- **NetBox Community Slack**: [netdev-community.slack.com](https://netdev.chat/)

## Credits

Based on the [NetBox plugin demo](https://github.com/netbox-community/netbox-plugin-demo) and [plugin tutorial](https://github.com/netbox-community/netbox-plugin-tutorial).

Scaffolded with [Cookiecutter](https://github.com/audreyr/cookiecutter) and [`netbox-community/cookiecutter-netbox-plugin`](https://github.com/netbox-community/cookiecutter-netbox-plugin).
