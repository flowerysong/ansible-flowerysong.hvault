# -*- coding: utf-8 -*-
# Copyright: (c) 2021, Paul Arthur <paul.arthur@flowerysong.com>
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.six.moves.urllib.error import URLError

from ..module_utils.base import (
    HVaultClient,
    hvault_argument_spec,
)


def optspec_to_config(optspec, params, join_lists=False):
    config = {}
    for (k, conf) in optspec.items():
        v = params[k]
        if conf.get('type') == 'list' and join_lists:
            if v:
                config[k] = ','.join(v)
            else:
                config[k] = ''
        else:
            config[k] = v
    return config


class HVaultModule():
    def __init__(self, argspec, optspec):
        _argspec = hvault_argument_spec()
        _argspec.update(
            dict(
                mount_point=dict(),
                name=dict(
                    required=True,
                ),
                state=dict(
                    choices=['present', 'absent'],
                    default='present',
                ),
            )
        )
        _argspec.update(argspec)
        self.optspec = optspec
        _argspec.update(optspec)

        self.module = AnsibleModule(
            supports_check_mode=True,
            argument_spec=_argspec,
        )
        self.params = self.module.params
        self.client = HVaultClient(self.params, self.module)

    def mangle_config(self, config):
        return config

    def mangle_result(self, result):
        return result

    def run(self, path_fmt, config, result_key='role', bad_keys=None, join_lists=False):
        path = path_fmt.format(self.params['mount_point'].strip('/'), self.params['name'])
        self._path = path

        changed = False
        try:
            result = self.client.get(path, fatal=False)['data']
        except URLError:
            result = {}

        for key in bad_keys or []:
            result.pop(key, None)

        if self.params['state'] == 'absent':
            if result:
                changed = True
                if not self.module.check_mode:
                    self.client.delete(path)
            self.module.exit_json(changed=changed)

        config.update(optspec_to_config(self.optspec, self.params, join_lists))
        config = self.mangle_config(config)

        if config != result:
            changed = True
            if not self.module.check_mode:
                self.client.post(path, config)

        if self.module.check_mode:
            result = config
        else:
            result = self.client.get(path)['data']

        kwargs = {}
        kwargs[result_key] = self.mangle_result(result)
        self.module.exit_json(changed=changed, **kwargs)
