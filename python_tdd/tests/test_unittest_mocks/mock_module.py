import unittest.mock

def mock_function(return_value=None):
    return unittest.mock.MagicMock(return_value=return_value)

def mock(side_effect=None):
    return unittest.mock.Mock(side_effect=side_effect)