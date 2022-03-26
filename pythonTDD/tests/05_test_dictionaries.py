import unittest
import dictionaries


class TestDictionaries(unittest.TestCase):

    def test_dictionary_creation(self):
        self.assertEqual(dictionaries.a_dict(), {'key': 'value'})
        self.assertEqual(dictionaries.a_dict(), dict(key='value'))
        self.assertEqual(
            dictionaries.a_dict(), dictionaries.another_dict()
        )

    def test_create_dictionary_using_numbers_as_keys(self):
        self.assertEqual({1: 'boom'}, {1: 'boom'})

    def test_create_dictionary_using_boolean_as_keys(self):
        self.assertEqual({False: 'boom'}, {False: 'boom'})
        self.assertEqual({True: 'boom'}, {True: 'boom'})

    def test_create_dictionary_using_tuples_as_keys(self):
        self.assertEqual({(1, 2): 'value'}, {(1, 2): 'value'})

    def test_create_dictionary_using_lists_as_keys_raises_type_error(self):
        with self.assertRaises(TypeError):
            {[1, 2]: 'value'}

    def test_create_dictionary_using_sets_as_keys(self):
        with self.assertRaises(TypeError):
            {{1, 2}: 'value'}

    def test_create_dictionary_using_dicts_as_keys(self):
        a_dict = {'key': 'value'}
        with self.assertRaises(TypeError):
            {a_dict: 'value'}

    def test_create_dictionary_fromkeys(self):
        self.assertEqual(
            dict.fromkeys(['basic', 'crest']),
            {
                'basic': None, 'crest': None
            }
        )

    def test_accessing_dictionary_values(self):
        self.assertEqual(dictionaries.a_dict()['key'], 'value')

    def test_listing_dictionary_values(self):
        self.assertEqual(
            list(dictionaries.a_dict().values()), ['value']
        )

    def test_dictionaries_raise_key_error_when_key_does_not_exist(self):
        with self.assertRaises(KeyError):
            (dictionaries.a_dict()['nonexistent_key'])

    def test_how_to_get_value_when_key_does_not_exist(self):
        self.assertIsNone(
            dictionaries.a_dict().get('nonexistent_key')
        )
        self.assertIsNone(
            dictionaries.a_dict().get('nonexistent_key', None)
        )

    def test_how_to_get_default_value_when_key_does_not_exist(self):
        self.assertEqual(
            dictionaries.a_dict().get('nonexistent_key', 'me'),
            'me'
        )

    def test_listing_dictionary_keys(self):
        self.assertEqual(
            list(dictionaries.a_dict().keys()),
            ['key']
        )

    def test_listing_dictionary_items(self):
        self.assertEqual(
            list(dictionaries.a_dict().items()),
            [('key', 'value')]
        )

    def test_person_dictionary(self):
        self.assertEqual(
            list(dictionaries.person().keys()),
            [
                'first_name', 'last_name', 'year_of_birth',
                'sex', 'age'
            ]
        )
        self.assertEqual(
            list(dictionaries.person().values()),
            [
                'me', 'last_name', '1986', 'M', '34'
            ]
        )
        self.assertEqual(
            list(dictionaries.person().items()),
            [
                ('first_name', 'me'), ('last_name', 'last_name'),
                ('year_of_birth', '1986'), ('sex', 'M'),
                ('age', '34')
            ]
        )

    def test_person_factory(self):
        self.assertEqual(
            dictionaries.person_factory(
                first_name='sibling',
                last_name='last_name',
                year_of_birth=2022,
                sex='F',
            ),
            {
                'first_name': 'sibling',
                'last_name': 'last_name',
                'year_of_birth': 2022,
                'sex': 'F',
                'age': 2021-2022
            }
        )
        self.assertEqual(
            dictionaries.person_factory(
                first_name='me',
                last_name='last_name',
                year_of_birth=2021,
                sex='M',
            ),
            {
                'first_name': 'me',
                'last_name': 'last_name',
                'year_of_birth': 2021,
                'sex': 'M',
                'age': 2021-2021
            }
        )
        self.assertEqual(
            dictionaries.person_factory(
                first_name='child_a',
                year_of_birth=2014,
                sex='M',
            ),
            {
                'first_name': 'child_a',
                'last_name': 'last_name',
                'year_of_birth': 2014,
                'sex': 'M',
                'age': 2021-2014
            }
        )
        self.assertEqual(
            dictionaries.person_factory(
                first_name='child_b',
                year_of_birth=2000,
                sex='M',
            ),
            {
                'first_name': 'child_b',
                'last_name': 'last_name',
                'year_of_birth': 2000,
                'sex': 'M',
                'age': 2021-2000
            }
        )
        self.assertEqual(
            dictionaries.person_factory(
                first_name='person',
                year_of_birth=1900,
            ),
            {
                'first_name': 'person',
                'last_name': 'last_name',
                'year_of_birth': 1900,
                'sex': 'F',
                'age': 121
            }
        )

    def test_dictionary_methods(self):
        self.maxDiff = None
        self.assertEqual(
            dir(dictionaries.a_dict()),
            [
                '__class__',
                '__class_getitem__',
                   '__contains__',
                   '__delattr__',
                   '__delitem__',
                   '__dir__',
                   '__doc__',
                   '__eq__',
                   '__format__',
                   '__ge__',
                   '__getattribute__',
                   '__getitem__',
                   '__gt__',
                   '__hash__',
                   '__init__',
                   '__init_subclass__',
                   '__ior__',
                   '__iter__',
                   '__le__',
                   '__len__',
                   '__lt__',
                   '__ne__',
                   '__new__',
                   '__or__',
                   '__reduce__',
                   '__reduce_ex__',
                   '__repr__',
                   '__reversed__',
                   '__ror__',
                   '__setattr__',
                   '__setitem__',
                   '__sizeof__',
                   '__str__',
                   '__subclasshook__',
                   'clear',
                   'copy',
                   'fromkeys',
                   'get',
                   'items',
                   'keys',
                   'pop',
                   'popitem',
                   'setdefault',
                   'update',
                   'values'
            ]
        )

    def test_set_default_value_to_none_forgiven_key(self):
        test = {'bippity': 'boppity'}
        test.setdefault('nonexistent_key')
        self.assertEqual(
            test, {'bippity': 'boppity',
            'nonexistent_key': None}
        )

    def test_set_default_value_when_default_value_given(self):
        test = {'bippity': 'boppity'}
        test.setdefault('nonexistent_key', 'default value')
        self.assertEqual(
            test, {'bippity': 'boppity',
            'nonexistent_key': 'default value'}
        )

    def test_set_default_vs_update(self):
        test = {
            'basic': 'crest',
            'whitening': 'colgate'
        }
        test.setdefault('non-basic', 'chewing stick')
        test.setdefault('browning', 'tobacco')
        test.setdefault('decaying', 'sugar')
        self.assertEqual(
            test,
            {
                'basic': 'crest',
                'whitening': 'colgate',
                'non-basic': 'chewing stick',
                'browning': 'tobacco',
                'decaying': 'sugar'
            }
        )

    def test_set_default_vs_update(self):
        test = {
            'basic': 'crest',
            'whitening': 'colgate'
        }
        test.update(
            {
                'non-basic': 'chewing stick',
                'browning': 'tobacco',
                'decaying': 'sugar'
            }
        )
        self.assertEqual(
            test,
            {
                'basic': 'crest',
                'whitening': 'colgate',
                'non-basic': 'chewing stick',
                'browning': 'tobacco',
                'decaying': 'sugar'
            }
        )

    def test_popitem(self):
        test = {
            'basic': 'crest',
            'whitening': 'colgate',
            'non-basic': 'chewing stick',
            'browning': 'tobacco',
            'decaying': 'sugar'
        }
        test.popitem()
        self.assertEqual(
            test,
            {
                'basic': 'crest',
                'whitening': 'colgate',
                'non-basic': 'chewing stick',
                'browning': 'tobacco',
            }
        )

    def test_pop(self):
        test = {
                'basic': 'crest',
                'whitening': 'colgate',
                'non-basic': 'chewing stick',
                'browning': 'tobacco',
                'decaying': 'sugar'
            }
        test.pop('non-basic')
        self.assertEqual(
            test,
            {
                'basic': 'crest',
                'whitening': 'colgate',
                'browning': 'tobacco',
                'decaying': 'sugar'
            }
        )
