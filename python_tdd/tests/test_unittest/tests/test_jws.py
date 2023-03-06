import botocore.stub
import unittest
import jws


class TestJWS(unittest.TestCase):

    def test_describe_instances(self):
        self.maxDiff = None
        with botocore.stub.Stubber(jws.EC2) as mock_ec2:
            mock_ec2.add_response(
                'describe_instances',
                {'bob': 'barker'}
            )
            self.assertEqual(
                jws.describe_instances(),
                {}
            )