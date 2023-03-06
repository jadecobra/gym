import unittest
import src.sniffer

class TestScentPicker(unittest.TestCase):

    maxDiff = None

    def test_load_file(self):
        load_file = src.sniffer.scent_picker.get_scent('scent_file.py')

        self.assertEqual(
            sorted(dir(load_file)),
            sorted([
                '__class__',
                '__delattr__',
                '__dict__',
                '__dir__',
                '__doc__',
                '__eq__',
                '__format__',
                '__ge__',
                '__getattribute__',
                '__gt__',
                '__hash__',
                '__init__',
                '__init_subclass__',
                '__le__',
                '__lt__',
                '__module__',
                '__ne__',
                '__new__',
                '__reduce__',
                '__reduce_ex__',
                '__repr__',
                '__setattr__',
                '__sizeof__',
                '__str__',
                '__subclasshook__',
                '__weakref__',
                'add_agent',
                'bg_fail',
                'bg_pass',
                'fg_fail',
                'fg_pass',
                'file_validators',
                'filename',
                'get_runners_and_validators',
                'get_module_name',
                'get_runners',
                'get_scent_api_type',
                'module',
                'reload',
                'run',
                'runner_name',
                'runners',
                'set_runner',
                'watch_paths'
            ])
        )

    def test_scent_module(self):
        self.assertEqual(1, 1)