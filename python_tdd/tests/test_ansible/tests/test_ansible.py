import jadecobra.toolkit
import json
import random
import subprocess
import unittest
import os


class TestAnsible(jadecobra.toolkit.TestCase):

    @staticmethod
    def run_module(arguments=None, filename=None):
        with open(filename, 'w') as args_file:
            args_file.write(json.dumps(arguments))
        return json.loads(
            subprocess.run(
                f'python tests/library/my_test.py {filename}',
                shell=True,
                capture_output=True,
            ).stdout.decode()
        )

    def test_creating_a_module(self):
        name = 'name'
        new = random.choice((True, False))
        arguments = {
            'ANSIBLE_MODULE_ARGS': {
                'name': name,
                'new': new
            },
        }

        self.assertEqual(
            self.run_module(
                arguments=arguments,
                filename='/tmp/args.json'
            ),
            {
                'changed': new,
                'invocation': {
                    'module_args': {
                        'name': name,
                        'new': new
                    }
                },
                'message': 'goodbye',
                'original_message': name
            }
        )

    @unittest.skip
    def test_module_with_playbook(self):
        self.assertEqual(
            subprocess.run(
                f'ansible-playbook ./tests/testmod.yml',
                shell=True,
                capture_output=True,
            ).stderr.decode(),
            'boom'
        )

    @unittest.skip
    def test_sanity(self):
        self.assertEqual(
            subprocess.run(
                f'ansible-test sanity -v --venv --python 3.10 MODULE_NAME',
                shell=True,
                capture_output=True,
            ).stderr.decode(),
            'boom'
        )