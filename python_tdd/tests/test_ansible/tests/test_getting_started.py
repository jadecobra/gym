import jadecobra.toolkit
import subprocess
import unittest
import os


class TestGettingStarted(jadecobra.toolkit.TestCase):

    # How to ping all instances

    @unittest.skip
    def test_failure(self):
        self.assertEqual(
            subprocess.run('ansible all -m ping', shell=True, capture_output=True).stdout,
            ''
        )