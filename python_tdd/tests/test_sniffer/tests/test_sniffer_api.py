import unittest
import sniffer.api


class TestSelectRunnableDecorator(unittest.TestCase):

    def test_decorator_adds_runnable_name_to_wrapped_func(self):
        def ex_validator():
            pass

        validator = sniffer.api.select_runnable('tagged')(sniffer.api.file_validator(ex_validator))

        self.assertEqual(validator.runnable, 'tagged')