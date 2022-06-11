"""
AssertionError is raised when an assert statement is False

You can write assertions with the assert keyword
You can write assertions with self.assert<Assertion> using the unittest library

fix the failing statements below to make sure the assert statements are True
"""

import unittest


class TestAssertionError(unittest.TestCase):

    def test_assertion_errors_with_none(self):
        assert None == False        # the python assert keyword
        self.assertIsNone(None)     # the unittest library assert

        assert None != None
        self.assertIsNotNone(None)

    def test_assertion_errors_with_false(self):
        assert False == True
        self.assertFalse(True)

    def test_assertion_errors_with_true(self):
        assert True == False
        self.assertTrue(False)

    def test_assertion_errors_with_equality(self):
        assert 1 == 2
        self.assertEqual(False, True)

        assert "a" == "b"
        self.assertEqual("a", "b")

        assert (1, 2, 3) == (1, 2)
        self.assertEqual((1, 2, 3), (1, 2))

        assert [1, 2, 3] == [1, 2]
        self.assertEqual([1, 2, 3], [1, 2])

        assert {1, 2} == {1, 2, 3}
        self.assertEqual({1, 2}, {1, 2, 3})

        assert {"a": 1, "b": 2, "c": 3} == dict(a=1, b=2)
        self.assertEqual({"a": 1, "b": 2, "c": 3}, dict(a=1, b=2))

        assert None != None
        self.assertNotEqual(None, None)

        assert False != False
        self.assertNotEqual(False, False)

        assert 1 != 1
        self.assertNotEqual(1, 1)

        assert "a" != "a"
        self.assertNotEqual("a", "a")

        assert (1, 2, 3) != (1, 2, 3)
        self.assertNotEqual((1, 2, 3), (1, 2, 3))

        assert [1, 2, 3] != [1, 2]
        self.assertNotEqual([1, 2, 3], [1, 2])

        assert {1, 2} != {1, 2, 3}
        self.assertNotEqual({1, 2}, {1, 2, 3})

        assert {"a": 1, "b": 2} != dict(a=1, b=2)
        self.assertNotEqual({"a": 1, "b": 2, "c": 3}, dict(a=1, b=2))