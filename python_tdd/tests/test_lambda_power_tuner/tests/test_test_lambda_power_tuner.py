import unittest
import jadecobra.toolkit

class TestLambdaPoweTuner(jadecobra.toolkit.TestCase):

    def test_failure(self):
        self.assertTrue(True)

    def test_z_commit(self):
        jadecobra.toolkit.git_push()