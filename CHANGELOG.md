# Changelog
All notable changes to this project will be documented in this file.

## [0.2.0] - 2021-04-28

### Added
- `aws_auth_role` module.
- `aws_secret_role_iam` module.
- `aws_secret_role_sts` module.
- `ldap_config` module.
- `ldap_group` module.
- `ldap_user` module.

### Changed
- Added more information to the module return when an HTTP error causes the
  module to fail.
- Renamed the `url` parameter to `vault_addr`.

## [0.1.0] - 2021-04-21

Initial Release
