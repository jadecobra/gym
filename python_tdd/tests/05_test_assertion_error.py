"""
AssertionError is raised when an assert statement is False
fix the failing statements below to make sure the assert statements are True
"""

import unittest


class TestAssertionError(unittest.TestCase):
    def test_python_assertion_errors(self):
        assert None == False
        assert False == True
        assert 1 == 2
        assert "a" == "b"
        assert (1, 2, 3) == (1, 2)
        assert [1, 2, 3] == [1, 2]
        assert {1, 2} == {1, 2, 3}
        assert {"a": 1, "b": 2, "c": 3} == dict(a=1, b=2)
        assert None != None
        assert False != False
        assert 1 != 1
        assert "a" != "a"
        assert (1, 2, 3) != (1, 2, 3)
        assert [1, 2, 3] != [1, 2]
        assert {1, 2} != {1, 2, 3}
        assert {"a": 1, "b": 2} != dict(a=1, b=2)

    def test_unittest_assertion_errors(self):
        self.assertIsNone(None)
        self.assertEqual(False, True)
        self.assertEqual(1, 2)
        self.assertEqual("a", "b")
        self.assertEqual((1, 2, 3), (1, 2))
        self.assertEqual([1, 2, 3], [1, 2])
        self.assertEqual({1, 2}, {1, 2, 3})
        self.assertEqual({"a": 1, "b": 2, "c": 3}, dict(a=1, b=2))
        self.assertNotEqual(None, None)
        self.assertNotEqual(False, False)
        self.assertNotEqual(1, 1)
        self.assertNotEqual("a", "a")
        self.assertNotEqual((1, 2, 3), (1, 2, 3))
        self.assertNotEqual([1, 2, 3], [1, 2])
        self.assertNotEqual({1, 2}, {1, 2, 3})
        self.assertNotEqual({"a": 1, "b": 2}, dict(a=1, b=2))
