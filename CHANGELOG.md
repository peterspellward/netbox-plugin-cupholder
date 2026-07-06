# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2026-07-06

Initial release.

### Added

- Cupholder model with rack mounting (front, left, or right side)
- CupholderType catalog with 12 seeded types (size, material, description)
- One cup holder per rack (OneToOneField)
- Full CRUD for cup holders and cup holder types through NetBox UI
- Rack detail page integration showing installed cup holder
- Change logging, journaling, custom fields, and tags
- REST API endpoints (`/cup-holders/`, `/cup-holder-types/`)
- GraphQL queries for types and instances
- Comprehensive test suite and MkDocs documentation
