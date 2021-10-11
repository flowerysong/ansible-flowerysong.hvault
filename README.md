# HashiCorp Vault Ansible Plugins

[![ansible-test](https://github.com/flowerysong/ansible-flowerysong.hvault/actions/workflows/ansible-test.yml/badge.svg)](https://github.com/flowerysong/ansible-flowerysong.hvault/actions/workflows/ansible-test.yml)

This [Ansible](https://www.ansible.com/) Collection implements
a number of plugins for interacting with [HashiCorp
Vault](https://vaultproject.io/). A complete set of low-level
operations (read, write, list, and delete) are available, so
functionality which does not yet have a higher-level interface should
still be possible to use. The implementation of high-level interfaces
prioritizes the subset of Vault functionality that I use.

## Dependencies

These plugins use standard Ansible features and require no extra
dependencies on the control node or target.

## Supported Ansible Versions

This collection is tested against the stable-2.11, stable-2.12, and
devel branches of ansible-core. Other versions may or may not work.

Controller-only plugins like lookups are tested with Python 3.6, 3.7,
3.8, and 3.9. Modules are tested with the same versions, plus Python
2.7.

## Supported Vault Versions

This collection is tested against the last three major versions of
Vault (currently 1.6, 1.7, and 1.8.) Older versions may or may not
work.

Some plugin interfaces include features specific to Vault Enterprise,
but no attempts are made to test that functionality.

## Where's the Documentation?

Documentation is not yet being built. If you have the collection
installed you can access each plugin's documentation via the
ansible-doc command, e.g. `ansible-doc flowerysong.hvault.engine` or
`ansible-doc -t lookup flowerysong.hvault.read`
