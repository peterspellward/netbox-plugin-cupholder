# Testing Guide for NetBox Cup Holder Plugin

This guide explains how to write and run tests for NetBox Cup Holder Plugin.

## Test Structure

Tests are organized in the `netbox_cup_holder_plugin/tests/` directory:

```
netbox_cup_holder_plugin/
├── tests/
│   ├── __init__.py
│   ├── test_models.py     # Model tests
│   ├── test_views.py      # Web view tests
│   ├── test_api.py        # REST API tests
│   └── test_graphql.py    # GraphQL queries
└── testing/
    ├── __init__.py        # Base test classes
    └── utils.py           # Test utilities
```

## Base Test Classes

This plugin provides standalone base test classes that encapsulate common testing patterns without depending on NetBox's internal testing utilities.

### PluginTestCase

Base class for all tests with user management and permissions.

```python
from netbox_cup_holder_plugin.testing import PluginTestCase

class MyTestCase(PluginTestCase):
    def test_something(self):
        # self.user is automatically created
        # self.client is logged in
        self.add_permissions(
            'netbox_cup_holder_plugin.view_cupholder',
            'netbox_cup_holder_plugin.view_cupholdertype',
        )
        # ... test code ...
```

**Key features:**
- Automatic test user creation
- Permission management (`add_permissions`, `remove_permissions`)
- Enhanced HTTP status assertions
- Transaction-based subtests with automatic cleanup

### PluginModelTestCase

For testing models with instance comparison utilities.

```python
from netbox_cup_holder_plugin.testing import PluginModelTestCase

class MyModelTestCase(PluginModelTestCase):
    def test_model(self):
        instance = MyModel.objects.first()

        # Compare instance to expected data
        self.assertInstanceEqual(
            instance,
            {'name': 'Expected', 'value': 123},
            exclude={'created', 'last_updated'}
        )

        # Convert instance to dict
        data = self.model_to_dict(instance)
```

**Key features:**
- `assertInstanceEqual()` - Compare model instances to dictionaries
- `model_to_dict()` - Convert instances to dictionaries
- Handles ForeignKey and ManyToMany relationships automatically

### PluginAPITestCase

For testing REST API endpoints.

```python
from netbox_cup_holder_plugin.testing import PluginAPITestCase

class MyAPITestCase(PluginAPITestCase):
    def setUp(self):
        super().setUp()
        self.list_url_name = 'plugins-api:netbox_cup_holder_plugin-api:mymodel-list'
        self.detail_url_name = 'plugins-api:netbox_cup_holder_plugin-api:mymodel-detail'

    def test_list(self):
        url = self._get_list_url()
        response = self.client.get(url)
        self.assertHttpStatus(response, 200)
```

**Key features:**
- APIClient with token authentication
- URL generation helpers (`_get_list_url`, `_get_detail_url`)
- Enhanced JSON response assertions

### PluginViewTestCase

For testing web views and forms.

```python
from netbox_cup_holder_plugin.testing import PluginViewTestCase

class MyViewTestCase(PluginViewTestCase):
    def setUp(self):
        super().setUp()
        self.base_url = 'plugins:netbox_cup_holder_plugin:mymodel'

    def test_create(self):
        url = self._get_url('add')
        form_data = self.post_data({'name': 'Test'})
        response = self.client.post(url, form_data)
        self.assertHttpStatus(response, 302)
```

**Key features:**
- URL generation (`_get_url`)
- Form data handling (`post_data`)
- Support for create/edit/delete views

### PluginGraphQLTestCase

For testing GraphQL queries.

```python
from netbox_cup_holder_plugin.testing import PluginGraphQLTestCase

class MyGraphQLTestCase(PluginGraphQLTestCase):
    def test_query(self):
        query = '''
        query {
            mymodel_list {
                id
                name
            }
        }
        '''
        response = self.execute_query(query)
        self.assertGraphQLSuccess(response)
```

## Test Utilities

The `netbox_cup_holder_plugin.testing.utils` module provides helpful utilities:

```python
from netbox_cup_holder_plugin.testing.utils import (
    get_random_string,       # Generate random test data
    create_test_user,        # Create users with permissions
    create_rack,             # Create a DCIM rack
    create_cupholder_type,   # Create a catalog type
    create_cupholder,        # Create an installed cup holder
    post_data,               # Convert dict to form POST format
    extract_form_errors,     # Parse form validation errors
    disable_warnings,        # Suppress expected log warnings
    create_tags,             # Create test tags
    get_deletable_objects,   # Check cascade deletion
    assert_object_changes,   # Verify change logging
)

# Example usage
name = get_random_string(20)
user = create_test_user(permissions=[
    'netbox_cup_holder_plugin.view_cupholder',
    'netbox_cup_holder_plugin.view_cupholdertype',
    'dcim.view_rack',
])
cupholder = create_cupholder(name='Test Cupholder')
tags = create_tags(['important', 'test'])

with disable_warnings('django.request'):
    response = self.client.get(url)  # Expected 403
```

## Running Tests

### Before you push (recommended)

CI uses **Ruff 0.11.12**, **NetBox v4.5.10**, and **`testing/configuration.py`** — not your day-to-day NetBox install. Run the same checks locally:

```bash
# Full CI parity (PostgreSQL + Redis on localhost required)
make ci

# Fast pre-push smoke test (lint + migration dependency graph only)
make ci-quick

# Install git hook to run ci-quick automatically on push
make install-pre-push-hook
```

`make ci-quick` catches the issues that slipped through earlier:

- Ruff version / rule mismatches vs CI
- Plugin migrations referencing NetBox core migrations that do not exist in v4.5.10
- (with `make ci`) bad `testing/configuration.py`, missing migrations, test failures

The NetBox release used for checks defaults to `v4.5.10` (see `.github/workflows/ci.yaml`). Override with `NETBOX_REF=v4.5.0 make ci-quick`.

### Locally (with NetBox installed)

```bash
# From your NetBox installation directory
cd /path/to/netbox/netbox

# Run all plugin tests (uses the plugin's minimal test configuration)
NETBOX_CONFIGURATION=netbox_cup_holder_plugin.test_configuration \
  python manage.py test netbox_cup_holder_plugin.tests

# Run specific test file
NETBOX_CONFIGURATION=netbox_cup_holder_plugin.test_configuration \
  python manage.py test netbox_cup_holder_plugin.tests.test_models

# Run specific test class
NETBOX_CONFIGURATION=netbox_cup_holder_plugin.test_configuration \
  python manage.py test netbox_cup_holder_plugin.tests.test_models.CupholderTestCase

# Run specific test method
NETBOX_CONFIGURATION=netbox_cup_holder_plugin.test_configuration \
  python manage.py test netbox_cup_holder_plugin.tests.test_models.CupholderTestCase.test_create

# Run with verbose output
NETBOX_CONFIGURATION=netbox_cup_holder_plugin.test_configuration \
  python manage.py test netbox_cup_holder_plugin.tests -v 2

# Run in parallel (faster)
NETBOX_CONFIGURATION=netbox_cup_holder_plugin.test_configuration \
  python manage.py test netbox_cup_holder_plugin.tests --parallel

# Keep database between runs (faster during development)
NETBOX_CONFIGURATION=netbox_cup_holder_plugin.test_configuration \
  python manage.py test netbox_cup_holder_plugin.tests --keepdb
```

### With Docker Compose (recommended for contributors)

```bash
# Build and start services
docker-compose up -d

# Run tests
docker-compose exec netbox python manage.py test netbox_cup_holder_plugin.tests

# Run specific tests
docker-compose exec netbox python manage.py test netbox_cup_holder_plugin.tests.test_api

# Stop services
docker-compose down
```

### CI/CD (GitHub Actions)

Tests run automatically on:
- Push to main or develop branches
- Pull requests

The CI workflow:
1. Runs code quality checks (Ruff)
2. Tests on Python 3.12, 3.13, 3.14
3. Uses PostgreSQL and Redis services
4. Checks for missing migrations
5. Runs full test suite with parallel execution

## Writing Tests

### Test Organization

Organize tests by functionality:

- `test_models.py` — model creation, validation, relationships, seed data
- `test_views.py` — web UI, forms, permissions
- `test_api.py` — REST API endpoints and filters
- `test_graphql.py` — GraphQL queries for types and instances

### Test Naming Convention

- Test classes: `<Model>TestCase`, `<Model>APITestCase`, `<Model>ViewTestCase`
- Test methods: `test_<action>_<scenario>`

Examples:
```python
def test_create_model_with_tags()
def test_list_without_permission()
def test_bulk_update_via_api()
```

### Testing Permissions

Always test both with and without permissions:

```python
def test_view_without_permission(self):
    """Test that view requires permission."""
    url = reverse('...')
    with disable_warnings('django.request'):
        response = self.client.get(url)
        self.assertHttpStatus(response, 403)

def test_view_with_permission(self):
    """Test view with proper permission."""
    self.add_permissions(
        'netbox_cup_holder_plugin.view_cupholder',
        'netbox_cup_holder_plugin.view_cupholdertype',
        'dcim.view_rack',
    )
    url = reverse('...')
    response = self.client.get(url)
    self.assertHttpStatus(response, 200)
```

### Testing Multiple Scenarios

Use `cleanupSubTest` for testing multiple scenarios with automatic database cleanup:

```python
def test_multiple_scenarios(self):
    scenarios = [
        ('with_tags', {'name': 'Test', 'tags': [tag1, tag2]}),
        ('without_tags', {'name': 'Test', 'tags': []}),
        ('with_description', {'name': 'Test', 'description': 'Desc'}),
    ]

    for name, data in scenarios:
        with self.cleanupSubTest(scenario=name):
            instance = MyModel.objects.create(**data)
            # Test assertions here
            # Database changes will be rolled back after this block
```

### Testing Forms

```python
def test_form_validation(self):
    """Test form validation."""
    url = reverse('netbox_cup_holder_plugin:mymodel_add')

    # Test with invalid data
    bad_data = self.post_data({'name': ''})
    response = self.client.post(url, bad_data)
    self.assertHttpStatus(response, 200)  # Form redisplay

    errors = extract_form_errors(response)
    self.assertIn('name', errors)
```

### Testing API Endpoints

```python
def test_api_crud(self):
    """Test complete CRUD cycle via API."""
    # Create
    url = self._get_list_url()
    data = {'name': 'Test'}
    response = self.client.post(url, data, format='json')
    self.assertHttpStatus(response, 201)

    # Read
    instance_id = response.data['id']
    detail_url = self._get_detail_url(instance_id)
    response = self.client.get(detail_url)
    self.assertHttpStatus(response, 200)

    # Update
    response = self.client.patch(detail_url, {'name': 'Updated'}, format='json')
    self.assertHttpStatus(response, 200)

    # Delete
    response = self.client.delete(detail_url)
    self.assertHttpStatus(response, 204)
```

## Test Configuration

The plugin ships with a minimal test configuration at `netbox_cup_holder_plugin/test_configuration.py`, which extends NetBox's built-in testing defaults and enables the plugin.

For standalone development, a fuller example configuration is also provided at `testing/configuration.py` (PostgreSQL, Redis, GraphQL enabled).

Set `NETBOX_CONFIGURATION=netbox_cup_holder_plugin.test_configuration` when running tests locally.

Environment variables to override database and Redis settings:

```bash
export DB_HOST=postgres
export DB_PORT=5432
export REDIS_HOST=redis
```

## Continuous Integration

The `.github/workflows/ci.yaml` workflow runs tests automatically:

```yaml
jobs:
  lint:    # Code quality checks
  test:    # Tests on Python 3.12, 3.13, 3.14
```

Tests must pass before PRs can be merged.

## Best Practices

1. **Use setUpTestData for shared fixtures** - Faster than setUp
2. **Test both positive and negative cases** - Success and failure
3. **Test permissions** - Always test without and with permissions
4. **Use meaningful test names** - Describe what's being tested
5. **Keep tests isolated** - Tests should not depend on each other
6. **Clean up test data** - Use cleanupSubTest for multiple scenarios
7. **Test edge cases** - Empty strings, None values, max lengths
8. **Use factories/utilities** - Don't repeat object creation code
9. **Test validation** - Both model and form validation
10. **Document complex tests** - Add docstrings explaining purpose

## Troubleshooting

**"No module named 'netbox_cup_holder_plugin'"**
- Ensure plugin is installed: `pip install -e .`
- Ensure plugin is in PLUGINS list in configuration.py

**"Table does not exist"**
- Run migrations: `python manage.py migrate`

**"Permission denied"**
- Ensure you added required permissions in setUp
- Cup holder tests often need `view_cupholdertype` and `dcim.view_rack` in addition to `view_cupholder`
- Check permission strings are correct

**Tests hanging**
- Check database/Redis connectivity
- Ensure services are running

**Random test failures**
- Check for test interdependencies
- Use --keepdb flag carefully (may have stale data)
- Ensure proper transaction cleanup

## Additional Resources

- [Django Testing Documentation](https://docs.djangoproject.com/en/stable/topics/testing/)
- [Django REST Framework Testing](https://www.django-rest-framework.org/api-guide/testing/)
- [NetBox Plugin Development](https://netboxlabs.com/docs/netbox/plugins/development/)
