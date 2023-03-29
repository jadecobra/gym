import unittest
import jadecobra.toolkit
import jadecobra.aws_lambda
import lambda_power_tuner

class TestLambdaPoweTuner(jadecobra.toolkit.TestCase):

    region = "us-east-1"
    account = "012345678901"
    function_name = "lambda_function_name"

    def lambda_function_arn(self):
        return jadecobra.aws_lambda.get_arn(
            name=self.function_name,
            region=self.region,
            account=self.account,
        )

    def test_arn(self):
        self.assertEqual(
            self.lambda_function_arn(),
            f"arn:aws:lambda:{self.region}:{self.account}:function:{self.function_name}"
        )

    def test_power_tuner_interface(self):
        number = 50
        payload = {}
        memory = [128, 256, 512, 1024]

        self.assertEqual(
            lambda_power_tuner.create_configuration(
                arn=self.lambda_function_arn(),
                memory=memory,
                number=number,
                payload=payload
            ),
            {
                "lambdaARN": self.lambda_function_arn(),
                "powerValues": memory,
                "num": number,
                "payload": payload
            }
        )
        self.assertTrue(True)

    def test_z_commit(self):
        jadecobra.toolkit.git_push()