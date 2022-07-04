import unittest
import datetime
import botocore.stub
import boto3


class TestBotocoreStubber(unittest.TestCase):

    def test_botocore_stubber(self):
        expected = {
            'IsTruncated': False,
            'Name': 'test-bucket',
            'MaxKeys': 1000,
            'Prefix': '',
            'Contents': [{
                'Key': 'test.txt',
                'ETag': '"abc123"',
                'StorageClass': 'STANDARD',
                'LastModified': datetime.datetime(2016, 1, 20, 22, 9),
                'Owner': {
                    'ID':  'abc123',
                    'DisplayName': 'myname'
                },
                'Size': 14814,
            }],
            'EncodingType': 'url',
            'ResponseMetadata': {
                'RequestId': 'abc123',
                'HTTPStatusCode': 200,
                'HostId': 'abc123',
            },
            'Marker': ''
        }

        s3 = boto3.client('s3')
        mock_s3 = botocore.stub.Stubber(s3)
        mock_s3.add_response(
            'list_objects',
            expected,
            {'Bucket': 'test-bucket'}
        )
        mock_s3.activate()

        self.assertEqual(
            s3.list_objects(Bucket='test-bucket'),
            expected
        )

    def test_botocore_stubber_as_context_manager(self):
        expected = {
            'Owner': {
                'ID': 'foo',
                'DisplayName': 'bar',
            },
            'Buckets': [{
                'CreationDate': datetime.datetime(2016, 1, 20, 22, 9),
                'Name': 'baz'
            }]
        }

        s3 = boto3.client('s3')
        with botocore.stub.Stubber(s3) as mock_s3:
            mock_s3.add_response(
                'list_buckets',
                expected,
                {}
            )

            self.assertEqual(
                s3.list_buckets(),
                expected
            )

    def test_using_stub_ANY_for_randomly_generated_values(self):
        expected = {
            'IsTruncated': False,
            'Name': 'test-bucket',
            'MaxKeys': 1000, 'Prefix': '',
            'Contents': [{
                'Key': 'test.txt',
                'ETag': '"abc123"',
                'StorageClass': 'STANDARD',
                'LastModified': datetime.datetime(2016, 1, 20, 22, 9),
                'Owner': {
                    'ID': 'abc123',
                    'DisplayName': 'myname'
                },
                'Size': 14814
            }],
            'EncodingType': 'url',
            'ResponseMetadata': {
                'RequestId': 'abc123',
                'HTTPStatusCode': 200,
                'HostId': 'abc123'
            },
            'Marker': ''
        }


        s3 = boto3.client('s3')
        with botocore.stub.Stubber(s3) as mock_s3:
            mock_s3.add_response(
                'list_objects',
                expected,
                {'Bucket': botocore.stub.ANY}
            )
            self.assertEqual(
                s3.list_objects(Bucket='test-bucket'),
                expected
            )
            self.maxDiff = None

    def test_stubber_attributes(self):
        ec2 = boto3.client('ec2')
        with botocore.stub.Stubber(ec2) as mock_ec2:
            self.assertEqual(
                dir(mock_ec2),
                [
                    '__class__',
                    '__delattr__',
                    '__dict__',
                    '__dir__',
                    '__doc__',
                    '__enter__',
                    '__eq__',
                    '__exit__',
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
                    '_add_response',
                    '_assert_expected_call_order',
                    '_assert_expected_params',
                    '_event_id',
                    '_expected_params_event_id',
                    '_get_response_handler',
                    '_queue',
                    '_should_not_stub',
                    '_validate_operation_response',
                    '_validate_response',
                    'activate',
                    'add_client_error',
                    'add_response',
                    'assert_no_pending_responses',
                    'client',
                    'deactivate'
                ]
            )