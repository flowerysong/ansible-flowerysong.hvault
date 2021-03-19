# HashiCorp Vault Ansible Plugins

[![CircleCI badge](https://circleci.com/gh/flowerysong/ansible-flowerysong.hvault.svg?style=shield)](https://circleci.com/gh/flowerysong/ansible-flowerysong.hvault)

This [Ansible](https://www.ansible.com/) Collection implements a number of
plugins for interacting with [HashiCorp Vault](https://vaultproject.io/).

These plugins use standard Ansible features and require no extra
dependency installation.

## Supported Ansible versions

This collection is currently tested against ansible-core 2.11 and
Python 3.8. Other versions may or may not work.

## Supported Vault versions

This collection is tested against the last three major versions of
Vault (currently 1.4, 1.5, and 1.6.) Older versions may or may not
work. Some plugin interfaces include features specific to Vault
Enterprise, but no attempts are made to test that functionality

## Where's the Documentation?

Documentation is not yet being built, but if you have the
collection installed you can access each plugin's documentation
via the ansible-doc command, e.g. `ansible-doc -t lookup
flowerysong.hvault.read`
