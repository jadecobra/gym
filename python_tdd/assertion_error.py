class TestAssertionError(unittest.TestCase):

    def test_assertion_errors_with_none(self):
        assert None == None        # the python assert keyword
        self.assertIsNone(None)     # the unittest library assert

        assert None == None
        self.assertIsNone(None)

    def test_assertion_errors_with_false(self):
        assert False == False
        self.assertFalse(False)

    def test_assertion_errors_with_true(self):
        assert True == True
        self.assertTrue(True)

    def test_assertion_errors_with_equality(self):
        assert False == False
        self.assertEqual(False, False)

        assert 1 == 1
        self.assertEqual(1, 1)

        assert "a" == "a"
        self.assertEqual("a", "a")

        assert (1, 2, 3) == (1, 2, 3)
        self.assertEqual((1, 2, 3), (1, 2, 3))

        assert [1, 2, 3] == [1, 2, 3]
        self.assertEqual([1, 2, 3], [1, 2, 3])

        assert {1, 2, 3} == {1, 2, 3}
        self.assertEqual({1, 2, 3}, {1, 2, 3})

        assert {"a": 1, "b": 2, "c": 3} == dict(a=1, b=2, c=3)
        self.assertEqual({"a": 1, "b": 2, "c": 3}, dict(a=1, b=2, c=3))

        assert None == None
        self.assertEqual(None, None)

        assert False == False
        self.assertEqual(False, False)

        assert 1 == 1
        self.assertEqual(1, 1)

        assert "a" == "a"
        self.assertEqual("a", "a")

        assert (1, 2, 3) == (1, 2, 3)
        self.assertEqual((1, 2, 3), (1, 2, 3))

        assert [1, 2, 3] == [1, 2, 3]
        self.assertEqual([1, 2, 3], [1, 2, 3])

        assert {1, 2, 3} == {1, 2, 3}
        self.assertEqual({1, 2, 3}, {1, 2, 3})

        assert {"a": 1, "b": 2} == dict(a=1, b=2)
        self.assertEqual({"a": 1, "b": 2}, dict(a=1, b=2))