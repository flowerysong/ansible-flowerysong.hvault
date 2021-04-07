# HashiCorp Vault Ansible Plugins

[![ansible-test](https://github.com/flowerysong/ansible-flowerysong.hvault/actions/workflows/ansible-test.yml/badge.svg)](https://github.com/flowerysong/ansible-flowerysong.hvault/actions/workflows/ansible-test.yml)

This [Ansible](https://www.ansible.com/) Collection implements a number of
plugins for interacting with [HashiCorp Vault](https://vaultproject.io/).

## Dependencies

These plugins use standard Ansible features and require no extra
dependencies on the controller or target hosts.

## Supported Ansible Versions

This collection is tested with Python 3.8 on ansible-base 2.10,
ansible-core 2.11, and ansible-core devel. Other versions may or may
not work.

## Supported Vault Versions

This collection is tested against the last three major versions of
Vault (currently 1.5, 1.6, and 1.7.) Older versions may or may not
work.

Some plugin interfaces include features specific to Vault Enterprise,
but no attempts are made to test that functionality.

## Where's the Documentation?

Documentation is not yet being built. If you have the collection
installed you can access each plugin's documentation via the
ansible-doc command, e.g. `ansible-doc flowerysong.hvault.engine` or
`ansible-doc -t lookup flowerysong.hvault.read`
