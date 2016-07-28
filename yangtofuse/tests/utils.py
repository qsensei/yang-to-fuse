import json
import os
import subprocess

import yangtofuse.plugin

here = os.path.dirname(__file__)
models_dir = os.path.join(here, 'model')


class BaseTest(object):
    def run_fut(self, models, search_paths):
        cmd = [
            'pyang',
            '--plugindir', os.path.dirname(yangtofuse.plugin.__file__),
        ]
        if search_paths:
            cmd.extend(['-p', ':'.join(search_paths)])
        cmd.extend(['-f', 'qsensei-fuse'])
        cmd.extend(models)
        response = subprocess.check_output(cmd).decode('utf-8')
        return json.loads(response)
