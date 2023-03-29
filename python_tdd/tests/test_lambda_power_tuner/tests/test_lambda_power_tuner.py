import unittest
import jadecobra.toolkit
import lambda_power_tuner

class TestLambdaPoweTuner(jadecobra.toolkit.TestCase):

    def test_power_tuner_interface(self):
        number = 50
        payload = {}
        memory = [128, 256, 512, 1024]
        region = "us-east-1"
        account = "012345678901"
        function_name = "lambda_function_name"
        lambda_function_arn = f"arn:aws:lambda:{region}:{account}:function:{lambda_function_name}"
        self.assertEqual(
            lambda_power_tuner.create_configuration(
                arn=lambda_function_arn,
                memory=memory,
                number=number,
                payload=payload
            ),
            {
                "lambdaARN": lambda_function_arn,
                "powerValues": memory,
                "num": number,
                "payload": payload
            }
        )
        self.assertTrue(True)

    def test_z_commit(self):
        jadecobra.toolkit.git_push()