#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright: (c) 2021, Paul Arthur <paul.arthur@flowerysong.com>
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = '''
module: ssh_role
author: "Paul Arthur (@flowerysong)"
short_description: Manage SSH roles in HashiCorp Vault
description:
  - Manage SSH signing roles in HashiCorp Vault.
  - This module only supports signed certificates, not OTP or Dynamic Key.
version_added: 0.1.0
extends_documentation_fragment:
  - flowerysong.hvault.base
options:
  mount_point:
    description:
      - Path where the SSH backend is mounted.
    type: str
    default: ssh
  name:
    description:
      - Name of the role to manage.
    type: str
    required: true
  state:
    description:
      - Desired state of the secret.
    type: str
    choices:
      - present
      - absent
    default: present
  default_user:
    description:
      - Default user to sign keys for.
    type: str
    default: ''
  allowed_users:
    description:
      - Users for which this role can sign keys.
      - Defaults to I(default_user) if this is not set and I(default_user) is.
    type: list
    elements: str
  allowed_domains:
    description:
      - Domains for which this role can sign keys.
    type: list
    elements: str
  ttl:
    description:
      - Default length of time the certificate will be valid, in seconds.
      - C(0) will use the system default.
    type: int
    default: 0
  max_ttl:
    description:
      - Maximum length of time a certificate can be valid, in seconds.
      - C(0) will use the system default.
    type: int
    default: 0
  allowed_critical_options:
    description:
      - Critical options a certificate can have when signed.
      - An empty list allows all options.
    type: list
    elements: str
  allowed_extensions:
    description:
      - Extensions a certificate can have when signed.
      - An empty list allows all extensions.
    type: list
    elements: str
  default_critical_options:
    description:
      - Options applied if none are provided in the signing request.
    type: dict
    default: {}
  default_extensions:
    description:
      - Extensions applied if none are provided in the signing request.
    type: dict
    default: {}
  allow_user_certificates:
    description:
      - Allows this role to sign user certificates.
      - Either this or I(allow_host_certificates) must be C(true) when I(state=present).
    type: bool
    default: false
  allow_host_certificates:
    description:
      - Allows this role to sign host certificates.
      - Either this or I(allow_user_certificates) must be C(true) when I(state=present).
    type: bool
    default: false
  allow_bare_domains:
    description:
      - Allows this role to sign host certificates for the domains specified in I(allowed_domains).
    type: bool
    default: false
  allow_subdomains:
    description:
      - Allows this role to sign host certificates for subdomains of the domains specified in I(allowed_domains).
    type: bool
    default: false
  allow_user_key_ids:
    description:
      - Allow signing requests to override the automatically generated key ID.
    type: bool
    default: false
  key_id_format:
    description:
      - Custom format for automatically generated key IDs.
      - Vault allows the variables C({{token_display_name}}), C({{role_name}}), and C({{public_key_hash}}) to be used.
    type: str
    default: ''
  allowed_user_key_lengths:
    description:
      - Mapping of SSH key types and their allowed sizes.
    type: dict
    default: {}
  algorithm_signer:
    description:
      - Algorithm to use when signing certificates.
      - Note that the default of C(rsa-sha2-512) is different from the upstream default, which is C(ssh-rsa) for historical reasons.
    type: str
    choices:
      - ssh-rsa
      - rsa-sha2-256
      - rsa-sha2-512
    default: rsa-sha2-512
'''

EXAMPLES = '''
'''

RETURN = '''
'''

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.six.moves.urllib.error import URLError

from ..module_utils.base import (
    HVaultClient,
    hvault_argument_spec,
)


def main():
    argspec = hvault_argument_spec()

    argspec.update(
        dict(
            mount_point=dict(
                default='ssh',
            ),
            name=dict(
                required=True,
            ),
            state=dict(
                choices=['present', 'absent'],
                default='present',
            ),
        )
    )

    role_options = dict(
        default_user=dict(default=''),
        allowed_users=dict(
            type='list',
            elements='str',
        ),
        allowed_domains=dict(
            type='list',
            elements='str',
        ),
        ttl=dict(
            type='int',
            default=0,
        ),
        max_ttl=dict(
            type='int',
            default=0,
        ),
        allowed_critical_options=dict(
            type='list',
            elements='str',
        ),
        allowed_extensions=dict(
            type='list',
            elements='str',
        ),
        default_critical_options=dict(
            type='dict',
            default={},
        ),
        default_extensions=dict(
            type='dict',
            default={},
        ),
        allow_user_certificates=dict(
            type='bool',
            default=False,
        ),
        allow_host_certificates=dict(
            type='bool',
            default=False,
        ),
        allow_bare_domains=dict(
            type='bool',
            default=False,
        ),
        allow_subdomains=dict(
            type='bool',
            default=False,
        ),
        allow_user_key_ids=dict(
            type='bool',
            default=False,
            no_log=False,
        ),
        key_id_format=dict(
            default='',
            no_log=False,
        ),
        allowed_user_key_lengths=dict(
            type='dict',
            default={},
            no_log=False,
        ),
        algorithm_signer=dict(
            choices=['ssh-rsa', 'rsa-sha2-256', 'rsa-sha2-512'],
            default='rsa-sha2-512',
        ),
    )

    argspec.update(role_options)

    module = AnsibleModule(
        supports_check_mode=True,
        argument_spec=argspec,
    )

    client = HVaultClient(module.params, module)

    path = '{0}/roles/{1}'.format(module.params['mount_point'].rstrip('/'), module.params['name'])

    changed = False
    try:
        result = client.get(path, fatal=False)['data']
    except URLError:
        result = {}

    # key_bits has no meaning for CAs, but is returned anyway
    result.pop('key_bits', None)

    if module.params['state'] == 'absent':
        if result:
            changed = True
            if not module.check_mode:
                client.delete(path)
        module.exit_json(changed=changed)

    config = {
        'key_type': 'ca',
        'allowed_users_template': False,
    }

    for (k, conf) in role_options.items():
        v = module.params[k]
        if conf.get('type') == 'list':
            if v:
                config[k] = ','.join(v)
            else:
                config[k] = ''
        else:
            config[k] = v

    if config.get('default_user') and not config.get('allowed_users'):
        config['allowed_users'] = config['default_user']

    if '{{' in (config.get('allowed_users') or ''):
        config['allowed_users_template'] = True

    if not config['allow_host_certificates'] and not config['allow_user_certificates']:
        module.fail_json(msg="At least one of 'allow_host_certificates' and 'allow_user_certificates' must be true.")

    if config != result:
        changed = True
        if not module.check_mode:
            client.post(path, config)

    if module.check_mode:
        result = config
    else:
        result = client.get(path)['data']

    module.exit_json(changed=changed, role=result)


if __name__ == '__main__':
    main()
