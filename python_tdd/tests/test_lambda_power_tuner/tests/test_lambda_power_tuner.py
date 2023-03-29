import unittest
import jadecobra.toolkit
import lambda_power_tuner

class TestLambdaPoweTuner(jadecobra.toolkit.TestCase):

    def test_power_tuner_interface(self):
        num = 50
        payload = {}
        power_values = [128, 256, 512, 1024]
        arn = "your-lambda-function-arn"
        self.assertEqual(
            lambda_power_tuner.create_input(
                arn=arn,
                power_values=power_values,
                num=num,
                payload=payload
            ),
            {
                "lambdaARN": arn,
                "powerValues": power_values,
                "num": num,
                "payload": payload
            }
        )
        self.assertTrue(True)

    def test_z_commit(self):
        jadecobra.toolkit.git_push()