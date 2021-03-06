# (c) 2021 Paul Arthur MacIain
# -*- coding: utf-8 -*-
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)


from ansible.errors import AnsibleError
from ansible.module_utils.six.moves.urllib.error import URLError
from ansible.plugins.lookup import LookupBase
from ansible.utils.display import Display

from ..module_utils.base import (
    HVaultClient,
    hvault_argument_spec,
)

display = Display()


class HVaultLookupBase(LookupBase):
    def config_client(self):
        client_opts = {}
        for opt in hvault_argument_spec():
            client_opts[opt] = self.get_option(opt)

        self.client = HVaultClient(client_opts)

    def run(self, terms, variables=None, **kwargs):
        ret = []

        self.config_client()

        for term in terms:
            display.debug('flowerysong.hvault lookup term: {0}'.format(term))

            try:
                secret = self.client.get(term)
            except URLError as e:
                raise AnsibleError('Unable to fetch secret') from e

            display.vvvv('flowerysong.hvault lookup found {0}'.format(secret))

            if secret:
                if 'data' in secret and not self.get_option('raw'):
                    secret = secret['data']
                ret.append(secret)
            else:
                raise AnsibleError('Unable to find secret matching "{0}"'.format(term))

        return ret
