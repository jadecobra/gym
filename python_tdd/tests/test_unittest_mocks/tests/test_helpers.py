from ast import Assert
import unittest
import unittest.mock
import module
import urllib.request

from utilities import POSITIONAL_ARGUMENTS, KEYWORD_ARGUMENTS


class TestHelpers(unittest.TestCase):

    maxDiff = None

    def test_sentinel(self):
        real = module.Class()
        real.method = unittest.mock.Mock(name='method')
        real.method.return_value = unittest.mock.sentinel.some_object

        self.assertEqual(real.method(), unittest.mock.sentinel.some_object)

    def test_default(self):
        self.assertEqual(unittest.mock.DEFAULT, unittest.mock.sentinel.DEFAULT)

    def test_call(self):
        mocked_object = unittest.mock.MagicMock(return_value=None)
        mocked_object(*POSITIONAL_ARGUMENTS, **KEYWORD_ARGUMENTS)
        mocked_object()
        self.assertEqual(
            mocked_object.call_args_list,
            [
                unittest.mock.call(*POSITIONAL_ARGUMENTS, **KEYWORD_ARGUMENTS),
                unittest.mock.call()
            ]
        )

    def test_use_call_list_to_make_assertions_on_chained_calls(self):
        mock_object = unittest.mock.MagicMock()
        mock_object(1).method(arg='foo').other('bar')(2.0)
        call_list = unittest.mock.call(1).method(arg='foo').other('bar')(2.0)

        self.assertEqual(
            mock_object.mock_calls,
            call_list.call_list()
        )

    def test_call_args(self):
        mock_object = unittest.mock.MagicMock(return_value=None)
        mock_object(*POSITIONAL_ARGUMENTS, **KEYWORD_ARGUMENTS)
        self.assertEqual(
            mock_object.call_args,
            unittest.mock.call(*POSITIONAL_ARGUMENTS, **KEYWORD_ARGUMENTS)
        )
        self.assertEqual(
            mock_object.call_args.args,
            POSITIONAL_ARGUMENTS
        )
        self.assertEqual(
            mock_object.call_args.kwargs,
            KEYWORD_ARGUMENTS
        )

    def test_call_args_with_name(self):
        mock_object = unittest.mock.MagicMock()
        mock_object.foo(*POSITIONAL_ARGUMENTS, **KEYWORD_ARGUMENTS)
        self.assertEqual(
            mock_object.mock_calls,
            [
                unittest.mock.call.foo(
                    *POSITIONAL_ARGUMENTS,
                    **KEYWORD_ARGUMENTS
                )
            ]
        )

        name, positional_arguments, keyword_arguments = mock_object.mock_calls[0]
        self.assertEqual(name, 'foo')
        self.assertEqual(positional_arguments, POSITIONAL_ARGUMENTS)
        self.assertEqual(keyword_arguments, KEYWORD_ARGUMENTS)

    def test_using_any_to_ignore_certain_arguments(self):
        mock_object = unittest.mock.Mock(return_value=None)
        mock_object('foo', bar=object())
        mock_object.assert_called_once_with('foo', bar=unittest.mock.ANY)

    def test_using_any_in_comparisons(self):
        mock_object = unittest.mock.MagicMock(return_value=None)
        mock_object(1)
        mock_object(1, 2)
        mock_object(object())
        self.assertEqual(
            mock_object.mock_calls,
            [
                unittest.mock.call(1),
                unittest.mock.call(1, 2),
                unittest.mock.ANY
            ]
        )

    def test_filter_dir(self):
        self.assertEqual(
            sorted(dir(unittest.mock.Mock())),
            [
                'assert_any_call',
                'assert_called',
                'assert_called_once',
                'assert_called_once_with',
                'assert_called_with',
                'assert_has_calls',
                'assert_not_called',
                'attach_mock',
                'call_args',
                'call_args_list',
                'call_count',
                'called',
                'configure_mock',
                'method_calls',
                'mock_add_spec',
                'mock_calls',
                'reset_mock',
                'return_value',
                'side_effect'
            ]
        )

        self.assertEqual(
            sorted(dir(unittest.mock.Mock(spec=urllib.request))),
            [
                'AbstractBasicAuthHandler',
                'AbstractDigestAuthHandler',
                'AbstractHTTPHandler',
                'BaseHandler',
                'CacheFTPHandler',
                'ContentTooShortError',
                'DataHandler',
                'FTPHandler',
                'FancyURLopener',
                'FileHandler',
                'HTTPBasicAuthHandler',
                'HTTPCookieProcessor',
                'HTTPDefaultErrorHandler',
                'HTTPDigestAuthHandler',
                'HTTPError',
                'HTTPErrorProcessor',
                'HTTPHandler',
                'HTTPPasswordMgr',
                'HTTPPasswordMgrWithDefaultRealm',
                'HTTPPasswordMgrWithPriorAuth',
                'HTTPRedirectHandler',
                'HTTPSHandler',
                'MAXFTPCACHE',
                'OpenerDirector',
                'ProxyBasicAuthHandler',
                'ProxyDigestAuthHandler',
                'ProxyHandler',
                'Request',
                'URLError',
                'URLopener',
                'UnknownHandler',
                '__all__',
                '__builtins__',
                '__cached__',
                '__doc__',
                '__file__',
                '__loader__',
                '__name__',
                '__package__',
                '__spec__',
                '__version__',
                '_cut_port_re',
                '_ftperrors',
                '_get_proxies',
                '_get_proxy_settings',
                '_have_ssl',
                '_localhost',
                '_noheaders',
                '_opener',
                '_parse_proxy',
                '_proxy_bypass_macosx_sysconf',
                '_randombytes',
                '_safe_gethostbyname',
                '_splitattr',
                '_splithost',
                '_splitpasswd',
                '_splitport',
                '_splitquery',
                '_splittag',
                '_splittype',
                '_splituser',
                '_splitvalue',
                '_thishost',
                '_to_bytes',
                '_url_tempfiles',
                'addclosehook',
                'addinfourl',
                'assert_any_call',
                'assert_called',
                'assert_called_once',
                'assert_called_once_with',
                'assert_called_with',
                'assert_has_calls',
                'assert_not_called',
                'attach_mock',
                'base64',
                'bisect',
                'build_opener',
                'call_args',
                'call_args_list',
                'call_count',
                'called',
                'configure_mock',
                'contextlib',
                'email',
                'ftpcache',
                'ftperrors',
                'ftpwrapper',
                'getproxies',
                'getproxies_environment',
                'getproxies_macosx_sysconf',
                'hashlib',
                'http',
                'install_opener',
                'io',
                'localhost',
                'method_calls',
                'mock_add_spec',
                'mock_calls',
                'noheaders',
                'os',
                'parse_http_list',
                'parse_keqv_list',
                'pathname2url',
                'posixpath',
                'proxy_bypass',
                'proxy_bypass_environment',
                'proxy_bypass_macosx_sysconf',
                'quote',
                're',
                'request_host',
                'reset_mock',
                'return_value',
                'side_effect',
                'socket',
                'ssl',
                'string',
                'sys',
                'tempfile',
                'thishost',
                'time',
                'unquote',
                'unquote_to_bytes',
                'unwrap',
                'url2pathname',
                'urlcleanup',
                'urljoin',
                'urlopen',
                'urlparse',
                'urlretrieve',
                'urlsplit',
                'urlunparse',
                'warnings'
            ]
        )

    def test_filter_dir_set_to_false(self):
        unittest.mock.FILTER_DIR = False

        self.assertEqual(
            sorted(dir(unittest.mock.Mock())),
            [
                '_NonCallableMock__get_return_value',
                '_NonCallableMock__get_side_effect',
                '_NonCallableMock__return_value_doc',
                '_NonCallableMock__set_return_value',
                '_NonCallableMock__set_side_effect',
                '__call__',
                '__class__',
                '__delattr__',
                '__dict__',
                '__dir__',
                '__doc__',
                '__eq__',
                '__format__',
                '__ge__',
                '__getattr__',
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
                '_call_matcher',
                '_calls_repr',
                '_execute_mock_call',
                '_extract_mock_name',
                '_format_mock_call_signature',
                '_format_mock_failure_message',
                '_get_call_signature_from_name',
                '_get_child_mock',
                '_increment_mock_call',
                '_mock_add_spec',
                '_mock_call',
                '_mock_call_args',
                '_mock_call_args_list',
                '_mock_call_count',
                '_mock_called',
                '_mock_check_sig',
                '_mock_children',
                '_mock_delegate',
                '_mock_methods',
                '_mock_mock_calls',
                '_mock_name',
                '_mock_new_name',
                '_mock_new_parent',
                '_mock_parent',
                '_mock_return_value',
                '_mock_sealed',
                '_mock_side_effect',
                '_mock_unsafe',
                '_mock_wraps',
                '_spec_asyncs',
                '_spec_class',
                '_spec_set',
                '_spec_signature',
                'assert_any_call',
                'assert_called',
                'assert_called_once',
                'assert_called_once_with',
                'assert_called_with',
                'assert_has_calls',
                'assert_not_called',
                'attach_mock',
                'call_args',
                'call_args_list',
                'call_count',
                'called',
                'configure_mock',
                'method_calls',
                'mock_add_spec',
                'mock_calls',
                'reset_mock',
                'return_value',
                'side_effect'
            ]
        )
        self.assertEqual(
            vars(unittest.mock.Mock()),
            {
                '_mock_call_args': None,
                '_mock_call_args_list': [],
                '_mock_call_count': 0,
                '_mock_called': False,
                '_mock_children': {},
                '_mock_delegate': None,
                '_mock_methods': None,
                '_mock_mock_calls': [],
                '_mock_name': None,
                '_mock_new_name': '',
                '_mock_new_parent': None,
                '_mock_parent': None,
                '_mock_return_value': unittest.mock.sentinel.DEFAULT,
                '_mock_sealed': False,
                '_mock_side_effect': None,
                '_mock_unsafe': False,
                '_mock_wraps': None,
                '_spec_asyncs': [],
                '_spec_class': None,
                '_spec_set': None,
                '_spec_signature': None,
                'method_calls': []
            }
        )

    def test_mock_open_for_writing_files(self):
        with unittest.mock.patch(
            '__main__.open',
            unittest.mock.mock_open()
        ) as mock_object:
            with open('foo', 'w') as mock_file:
                mock_file.write('some stuff')

        self.assertEqual(mock_object.mock_calls, [])
        with self.assertRaises(AssertionError):
            mock_object.assert_called_once_with('foo', 'w')

    def test_mock_open_for_reading_files(self):
        with unittest.mock.patch(
            '__main__.open',
            unittest.mock.mock_open(read_data='bibble')
        ) as mock_object:
            with open('foo') as file:
                self.assertEqual(file.read(), 'some stuff')

        with self.assertRaises(AssertionError):
            mock_object.assert_called_once_with('foo')

    def test_sealing_mocks(self):
        mock_object = unittest.mock.Mock()
        mock_object.sub_mock.attribute_a = 1
        mock_object.not_sub_mock = unittest.mock.Mock(name='not_sub_mock')
        unittest.mock.seal(mock_object)

        with self.assertRaises(AttributeError):
            mock_object.new_attribute

        mock_object.sub_mock.attribute_b
        mock_object.not_sub_mock.attribute_a