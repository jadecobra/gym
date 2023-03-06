import unittest
import src.sniffer
import toolbox


class ScentModuleTest(unittest.TestCase):

    @staticmethod
    def get_scent(filename):
        return src.sniffer.scent_picker.get_scent(f'{filename}.py')

    def test_set_runner_and_get_runner_methods(self):
        filename = 'test_scent_file'
        extensions = [f'ext{i}' for i in range(3)]
        prefix = 'test'

        toolbox.create_scent(
            filename=filename,
            extensions=extensions,
            prefix=prefix,
        )
        scent = self.get_scent(filename)
        self.assertEqual(
            scent.get_runners(),
            scent.runners
        )

        for i, execution_type in enumerate(extensions):
            with self.subTest(i=execution_type):
                runner_name = f'{prefix}_{execution_type}'
                scent.set_runner(runner_name)
                self.assertEqual(scent.runner_name, runner_name)
                self.assertEqual(scent.get_runners(), (scent.runners[i],))

        execution_type = f'{prefix}_unknown'
        scent.set_runner(execution_type)
        self.assertEqual(scent.runner_name, execution_type)
        self.assertEqual(scent.get_runners(), ())
        toolbox.delete_scent('test_scent_file')

    def test_scent_module_interation_with_scanner(self):
        scent = self.get_scent('scent_file')
        scanner = src.sniffer.scanner.base.BaseScanner([], scent)

        for validator in scent.file_validators:
            scanner.add_validator(validator)

        self.assertTrue(scanner.is_valid_type('file.ext0'))
        self.assertTrue(scanner.is_valid_type('file.ext1'))
        self.assertTrue(scanner.is_valid_type('file.ext2'))
        self.assertTrue(scanner.is_valid_type('file.ext3'))
        self.assertFalse(scanner.is_valid_type('file.negative'))