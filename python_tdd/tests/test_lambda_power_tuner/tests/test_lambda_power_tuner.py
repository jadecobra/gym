import unittest
import jadecobra.toolkit
import jadecobra.aws_lambda
import lambda_power_tuner

class TestLambdaPoweTuner(jadecobra.toolkit.TestCase):

    region:str = "us-east-1"
    account:str = "012345678901"
    function_name:str = "lambda_function_name"
    invocations:int = 50
    payload:dict = {}
    memory_values:list = [128, 256, 512, 1024]
    lambda_function_arn:dict = jadecobra.aws_lambda.get_arn(
        name=function_name,
        region=region,
        account=account,
    )
    lambda_power_tuner = lambda_power_tuner.LambdaPowerTuner(
        arn=lambda_function_arn,
        memory_values=memory_values,
        invocations=invocations,
        payload=payload
    )

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
            memory=self.memory_values,
            invocations=self.invocations,
            payload=self.payload
        )

    def test_power_tuner_interface(self):
        self.assertEqual(
            self.lambda_power_tuner_configuration(),
            {
                "lambdaARN": self.lambda_function_arn(),
                "powerValues": self.memory_values,
                "num": self.invocations,
                "payload": self.payload
            }
        )

    def test_initializer(self):
        self.assertEqual(
            lambda_power_tuner.initializer(self.memory_values),
            self.memory_values
        )

    def test_executor(self):
        self.assertEqual(
            self.lambda_power_tuner.execute(
            ),
            [f'invoking {self.lambda_function_arn()}/{invocation}...' for invocation in range(self.invocations)]
        )

    def test_invocation(self):
        self.assertEqual(
            self.lambda_power_tuner.clean_up(),
            [f'deleting {self.lambda_function_arn()}/{invocation}...' for invocation in range(self.invocations)]
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