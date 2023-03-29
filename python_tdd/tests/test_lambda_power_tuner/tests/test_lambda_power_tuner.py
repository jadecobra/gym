import unittest
import jadecobra.toolkit
import jadecobra.aws_lambda
import lambda_power_tuner

class TestLambdaPoweTuner(jadecobra.toolkit.TestCase):

    region = "us-east-1"
    account = "012345678901"
    function_name = "lambda_function_name"
    number = 50
    payload = {}
    memory = [128, 256, 512, 1024]

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

    def lambda_power_tuner_configuration(self):
        return lambda_power_tuner.create_configuration(
            arn=self.lambda_function_arn(),
            memory=self.memory,
            invocations=self.number,
            payload=self.payload
        )

    def test_power_tuner_interface(self):
        self.assertEqual(
            self.lambda_power_tuner_configuration(),
            {
                "lambdaARN": self.lambda_function_arn(),
                "powerValues": self.memory,
                "num": self.number,
                "payload": self.payload
            }
        )

    def test_initializer(self):
        self.assertEqual(
            lambda_power_tuner.initializer(self.memory),
            self.memory
        )

    def test_executor(self):
        self.assertEqual(
            lambda_power_tuner.executor(
                invocationes=self.invocations,
                arn=self.lambda_function_arn()
            ),
            [
            
            ]
        )

    def test_power_tuner_output(self):
        self.assertEqual(
            lambda_power_tuner.optimize(
                self.lambda_power_tuner_configuration()
            ),
            {
                "results": {
                    "power": "128",
                    "cost": 0.0000002083,
                    "duration": 2.906,
                    "stateMachine": {
                        "executionCost": 0.00045,
                        "lambdaCost": 0.0005252,
                        "visualization": "https://lambda-power-tuning.show/#<encoded_data>"
                    }
                }
            }
        )

    def test_z_commit(self):
        jadecobra.toolkit.git_push()