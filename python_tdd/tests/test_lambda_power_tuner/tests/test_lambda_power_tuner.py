import unittest
import jadecobra.toolkit
import lambda_power_tuner

class TestLambdaPoweTuner(jadecobra.toolkit.TestCase):

    def test_power_tuner_interface(self):
        self.assertEqual(
            lambda_power_tuner.create_input(
                arn="your-lambda-function-arn",
                power_values=[128, 256, 512, 1024],
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