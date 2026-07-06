"""
Minimal NetBox configuration for running plugin tests.
"""

from netbox.configuration_testing import *  # noqa: F403

DEBUG = False

PLUGINS = [
    'netbox_cup_holder_plugin',
]
