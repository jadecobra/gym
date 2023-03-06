import os
import unittest


class TestBuild(unittest.TestCase):

    def test_z_build(self):
        os.system('python3 -m build')
        # os.system('python3 -m twine upload dist/*')
