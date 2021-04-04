# HashiCorp Vault Ansible Plugins

[![CircleCI badge](https://circleci.com/gh/flowerysong/ansible-flowerysong.hvault.svg?style=shield)](https://circleci.com/gh/flowerysong/ansible-flowerysong.hvault)

This [Ansible](https://www.ansible.com/) Collection implements a number of
plugins for interacting with [HashiCorp Vault](https://vaultproject.io/).

## Dependencies

These plugins use standard Ansible features and require no extra
dependencies on the controller or target hosts.

## Supported Ansible Versions

This collection is currently tested with ansible-core 2.11 and Python
3.8. Other versions may or may not work.

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
