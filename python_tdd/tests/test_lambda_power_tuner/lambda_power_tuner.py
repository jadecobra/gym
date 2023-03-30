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
        self.invocations = 5 if invocations < 5 else invocations
        self.payload = payload

    def create_aliases(self):
        return [f'{self.lambda_function_arn}/{invocation}' for invocation in range(self.invocations)]

    def initialize(self):
        '''Return N versions and aliases for each memory configuration'''
        return [item for item in self.memory_values]

    def execute(self, in_parallel:bool=False):
        '''Execute given lambda function N invocation times'''
        if in_parallel:
            return [f'invoking {version} in parallel for {memory}...' for version in self.create_aliases() for memory in self.memory_values]
        return [f'invoking {version}...' for version in self.create_aliases()]

    def clean_up(self):
        '''Delete all previous generated aliases and versions'''
        return [f'deleting {version}...' for version in self.create_aliases()]

    def analyze(self):
        return f'lowest_average_cost_per_invocation is ...{(self.invocations)}'

    def optimize(self, auto_optimize=False):
        return {
            "optimal_memory": 128,
            "average_cost_per_invocation": 0.0000002083,
            "average_duration_per_invocation": 2.906,
            "lambda_power_tuner": {
                "cost_of_power_tuner_execution": 0.00045,
                "cost_of_power_tuner_lambdas": 0.0005252,
                "visualization": "https://lambda-power-tuning.show/#<encoded_data>"
            }
        }

def create_configuration(arn:str=None, memory: list=None, invocations: int=None, payload:dict=None):
    return {
        "lambdaARN": arn,
        "powerValues": memory,
        "num": invocations,
        "payload": {} if not payload else payload
    }
