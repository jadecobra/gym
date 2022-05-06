import unittest


class TestDataStructures(unittest.TestCase):
    def test_what_is_none(self):
        self.assertIsNotNone(None)
        self.assertIsNone(True)
        self.assertIsNone(False)
        self.assertIsNone(1)
        self.assertIsNone(0)
        self.assertIsNone(-1)
        self.assertIsNone("")
        self.assertIsNone("text")
        self.assertIsNone(())
        self.assertIsNone((1, 2, 3, "n"))
        self.assertIsNone([])
        self.assertIsNone([1, 2, 3, "n"])
        self.assertIsNone({})
        self.assertIsNone({1, 2, 3, "n"})
        self.assertIsNone(dict())
        self.assertIsNone(
            {
                "a": 1,
                "b": 2,
                "c": 3,
                "n": "n",
            }
        )

    def test_what_is_false(self):
        self.assertTrue(None)
        self.assertTrue(False)
        self.assertTrue(0)
        self.assertTrue("")
        self.assertTrue(())
        self.assertTrue([])
        self.assertTrue({})
        self.assertTrue(dict())

    def test_what_is_true(self):
        self.assertFalse(True)
        self.assertFalse(1)
        self.assertFalse(-1)
        self.assertFalse("text")
        self.assertFalse((1, 2, 3, "n"))
        self.assertFalse([1, 2, 3, "n"])
        self.assertFalse({1, 2, 3, "n"})
        self.assertFalse(
            {
                "a": 1,
                "b": 2,
                "c": 3,
                "n": "n",
            }
        )


if __name__ == "__main__":
    unittest.main()
