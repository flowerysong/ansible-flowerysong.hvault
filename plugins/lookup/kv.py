# (c) 2021 Paul Arthur MacIain
# -*- coding: utf-8 -*-
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = """
name: kv
author: Paul Arthur (@flowerysong)
short_description: Lookup for HashiCorp Vault KV version 1 secrets
description:
  - Ansible lookup for HashiCorp Vault.
options:
  _terms:
    description:
      - Secrets to look up.
    required: True
  mount_point:
    description:
      - Path where the KV backend is mounted.
    default: secret
extends_documentation_fragment:
  - flowerysong.hvault.base
  - flowerysong.hvault.base.PLUGINS
"""

EXAMPLES = """
- name: Look up a secret
  debug:
    msg: The result is {{ lookup('flowerysong.hvault.kv', 'ping') }}
"""

RETURN = """
  _raw:
    description:
      - Secrets
    type: list
    elements: dict
"""

from ..plugin_utils.lookup import HVaultLookupBase


class LookupModule(HVaultLookupBase):
    def run(self, terms, variables=None, **kwargs):
        self.set_options(direct=kwargs)
        self.set_option('raw', False)

        mount = self.get_option('mount_point')
        terms = ['/'.join((mount, x)) for x in terms]

        return super(LookupModule, self).run(terms)
