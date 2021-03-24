# (c) 2021 Paul Arthur MacIain
# -*- coding: utf-8 -*-
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = """
name: kv
author: Paul Arthur (@flowerysong)
short_description: Lookup for HashiCorp Vault KV version 2
description:
  - Ansible lookup for HashiCorp Vault.
options:
  _terms:
    description:
      - Secrets to look up.
    required: True
  mount_point:
    description:
      - Path where the KV secrets engine is mounted
    default: secret
  version:
    description:
      - Requested version of the secret.
      - If not specified the latest version will be returned.
    type: int
extends_documentation_fragment:
  - flowerysong.hvault.base
  - flowerysong.hvault.base.PLUGINS
"""

EXAMPLES = """
- name: Look up a secret
  debug:
    msg: The result is {{ lookup('flowerysong.hvault.kv_v2', 'ping') }}

- name: Look up a specific version of a secret
  debug:
    msg: The result is {{ lookup('flowerysong.hvault.kv_v2', 'ping', version=2) }}
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
        version = self.get_option('version')
        version = '?version={0}'.format(version) if version else ''
        terms = ['{0}/data/{1}{2}'.format(mount, x, version) for x in terms]

        result = super(LookupModule, self).run(terms)
        return [x['data'] for x in result]
