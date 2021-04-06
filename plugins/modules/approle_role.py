#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright: (c) 2021, Paul Arthur <paul.arthur@flowerysong.com>
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = '''
module: approle_role
author: "Paul Arthur (@flowerysong)"
short_description: Manage AppRole roles in HashiCorp Vault
description:
  - Manage AppRole roles in HashiCorp Vault.
version_added: 0.1.0
extends_documentation_fragment:
  - flowerysong.hvault.base
  - flowerysong.hvault.role
options:
  mount_point:
    default: approle
  bind_secret_id:
    type: bool
    default: true
    description:
      - Whether a SecretID is required to authenticate.
  secret_id_bound_cidrs:
    type: list
    elements: str
    default: []
    description:
      - CIDR blocks that are allowed to authenticate.
  secret_id_num_uses:
    type: int
    default: 0
    description:
      - Number of times any particular SecretID can be used to authenticate.
      - C(0) is unlimited.
  secret_id_ttl:
    type: int
    default: 0
    description:
      - Duration in seconds after which a SecretID expires.
  token_ttl:
    type: int
    default: 0
    description:
      - The incremental lifetime for renewed tokens.
  token_max_ttl:
    type: int
    default: 0
    description:
      - The maximum lifetime for generated tokens.
  token_policies:
    type: list
    elements: str
    default: []
    description:
      - List of policies to add to generated tokens.
      - Depending on the auth method, this list may be supplemented by
        user/group/other values.
  token_bound_cidrs:
    type: list
    elements: str
    default: []
    description:
      - CIDR blocks that are allowed to authenticate.
      - The resulting token will also be tied to these blocks.
  token_explicit_max_ttl:
    type: int
    default: 0
    description:
      - Explicit max TTL for generated tokens.
      - This is a hard cap even if I(token_ttl) and I(token_max_ttl) would
        still allow a renewal.
  token_no_default_policy:
    type: bool
    default: false
    description:
      - Disable adding the default policy to generated tokens.
      - Normally this policy is added in addition to the explicit policies in
        I(token_policies).
  token_num_uses:
    type: int
    default: 0
    description:
      - The maximum number of times a generated token can be used.
      - C(0) is unlimited.
      - If this is set to a non-zero value the token will not be able to create
        child tokens.
  token_period:
    type: int
    default: 0
    description:
      - The period to set on the token.
  token_type:
    description:
      - Type of token that should be returned.
      - C(default) uses the setting from the mount.
    type: str
    choices:
      - default
      - service
      - batch
    default: default
'''

EXAMPLES = '''
'''

RETURN = '''
'''

from ..module_utils.module import HVaultModule


def main():
    argspec = dict(
        mount_point=dict(
            default='approle',
        ),
    )

    optspec = dict(
        bind_secret_id=dict(
            type='bool',
            default=True,
        ),
        secret_id_bound_cidrs=dict(
            type='list',
            elements='str',
            default=[],
            no_log=False,
        ),
        secret_id_num_uses=dict(
            type='int',
            default=0,
            no_log=False,
        ),
        secret_id_ttl=dict(
            type='int',
            default=0,
            no_log=False,
        ),
        token_ttl=dict(
            type='int',
            default=0,
            no_log=False,
        ),
        token_max_ttl=dict(
            type='int',
            default=0,
            no_log=False,
        ),
        token_policies=dict(
            type='list',
            elements='str',
            default=[],
            no_log=False,
        ),
        token_bound_cidrs=dict(
            type='list',
            elements='str',
            default=[],
            no_log=False,
        ),
        token_explicit_max_ttl=dict(
            type='int',
            default=0,
            no_log=False,
        ),
        token_no_default_policy=dict(
            type='bool',
            default=False,
            no_log=False,
        ),
        token_num_uses=dict(
            type='int',
            default=0,
            no_log=False,
        ),
        token_period=dict(
            type='int',
            default=0,
            no_log=False,
        ),
        token_type=dict(
            choices=[
                'default',
                'service',
                'batch',
            ],
            default='default',
            no_log=False,
        ),
    )

    module = HVaultModule(
        argspec=argspec,
        optspec=optspec,
    )

    module.run(
        path_fmt='auth/{0}/role/{1}',
        config=dict(),
        bad_keys=['local_secret_ids'],
    )


if __name__ == '__main__':
    main()
