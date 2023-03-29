import unittest
import jadecobra.toolkit

class TestLambdaPoweTuner(jadecobra.toolkit.TestCase):

    def test_power_tuner_interface(self):
        self.assertEqual(
            lambda_power_tuner.create_input(
                lambda_arn="your-lambda-function-arn",
                powerValues=[128, 256, 512, 1024],
                num=50,
                payload={}
            ),
            {
                "lambdaARN": "your-lambda-function-arn",
                "powerValues": [128, 256, 512, 1024],
                "num": 50,
                "payload": {}
            }
        )
        self.assertTrue(True)

    def test_z_commit(self):
        jadecobra.toolkit.git_push()