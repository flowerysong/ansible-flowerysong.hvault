#!/usr/bin/env python3

import copy
import json
import os
import subprocess
import sys

import yaml


runtime = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'meta/runtime.yml')

with open(runtime, 'r') as f:
    old = yaml.safe_load(f)

res = subprocess.run(['ansible-doc', '-t', 'module', '-l', 'flowerysong.hvault', '-j'], capture_output=True, text=True)

modules = list(json.loads(res.stdout))

new = copy.deepcopy(old)

new['action_groups'] = {
    'hvault': modules,
}

print(yaml.dump(new, indent=2))

if old != new:
    with open(runtime, 'w') as f:
        f.write(yaml.dump(new, indent=2))
