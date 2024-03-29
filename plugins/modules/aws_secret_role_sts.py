#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright: (c) 2021, Paul Arthur <paul.arthur@flowerysong.com>
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = '''
module: aws_secret_role_sts
author: "Paul Arthur (@flowerysong)"
short_description: Manage AWS STS secret roles in HashiCorp Vault
description:
  - Manage AWS STS secret roles in HashiCorp Vault.
  - The underlying API is the same one used by C(aws_secret_role_iam), so either
    module can delete roles created by the other.
seealso:
  - module: flowerysong.hvault.aws_secret_role_iam
version_added: 0.2.0
extends_documentation_fragment:
  - flowerysong.hvault.base
  - flowerysong.hvault.auth_token
  - flowerysong.hvault.role
options:
  mount_point:
    default: aws
  credential_type:
    type: str
    choices:
      - assumed_role
      - federation_token
    default: assumed_role
    description:
      - Type of credential to create.
  policy_arns:
    type: list
    elements: str
    description:
      - AWS managed policy ARNs used for filtering what the generated credentials can do.
  policy_document:
    type: str
    description:
      - Policy document used for filtering what the generated credentials can do.
  iam_groups:
    type: list
    elements: str
    description:
      - IAM groups whose permissions will be combined with I(policy_arns) and I(policy_document).
  role_arns:
    type: list
    elements: str
    description:
      - AWS roles this Vault role is allowed to assume.
      - Required when I(credential_type=assumed_role).
  default_sts_ttl:
    type: str
    description:
      - Default TTL for credentials when no TTL is supplied in the request.
  max_sts_ttl:
    type: str
    description:
      - Maximum TTL for credentials generated by this role.
'''

EXAMPLES = '''
'''

RETURN = '''
'''

from ..module_utils.module import HVaultModule


def main():
    argspec = dict(
        mount_point=dict(
            default='aws',
        ),
    )

    optspec = dict(
        credential_type=dict(
            choices=['assumed_role', 'federation_token'],
            default='assumed_role',
        ),
        role_arns=dict(
            type='list',
            elements='str',
        ),
        policy_arns=dict(
            type='list',
            elements='str',
        ),
        policy_document=dict(),
        iam_groups=dict(
            type='list',
            elements='str',
        ),
        default_sts_ttl=dict(),
        max_sts_ttl=dict(),
    )

    module = HVaultModule(
        argspec=argspec,
        optspec=optspec,
        required_if=[
            ['credential_type', 'federation_token', ['policy_arns', 'policy_document'], True],
        ],
    )

    module.run(
        path_fmt='{0}/roles/{1}',
        config=dict(
            user_path=None,
            permissions_boundary_arn=None,
        ),
    )


if __name__ == '__main__':
    main()
