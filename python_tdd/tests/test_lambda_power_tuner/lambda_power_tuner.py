class LambdaPowerTuner(object):

    def __init__(
        self,
        lambda_function_arn: str=None,
        memory_values: list=None,
        invocations: int=None,
        payload: dict=None,
    ):
        self.lambda_function_arn = lambda_function_arn
        self.memory_values = memory_values
        self.invocations = invocations
        self.payload = payload

    def create_aliases(self):
        return [f'{self.lambda_function_arn}/{invocation}' for invocation in range(self.invocations)]

    def initialize(self):
        '''Return N versions and aliases for each memory configuration'''
        return [item for item in self.memory_values]

    def execute(self, in_parallel:bool=False):
        '''Execute given lambda function N invocation times'''
        if in_parallel:
            return [f'invoking {self.lambda_function_arn}/{invocation} in parallel for {memory}...' for invocation in range(self.invocations) for memory in self.memory_values]
        return [f'invoking {self.lambda_function_arn}/{invocation}...' for invocation in range(self.invocations)]

    def clean_up(self):
        '''Delete all previous generated aliases and versions'''
        return [f'deleting {self.lambda_function_arn}/{invocation}...' for invocation in range(self.invocations)]

    def analyze(self):
        return f'lowest_average_cost_per_invocation is ...{(self.invocations)}'

    def optimize(self, auto_optimize=False):
        return {
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

def create_configuration(arn:str=None, memory: list=None, invocations: int=None, payload:dict=None):
    return {
        "lambdaARN": arn,
        "powerValues": memory,
        "num": invocations,
        "payload": {} if not payload else payload
    }
