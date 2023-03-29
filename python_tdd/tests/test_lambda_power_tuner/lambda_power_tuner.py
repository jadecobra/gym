class LambdaPowerTuner(object):

    def __init__(
        self,
        arn: str=None,
        memory: list=None,
        invocations: int=None,
        payload: dict=None,
    ):
        self.arn = arn
        self.memory = memory
        self.invocations = invocations
        self.payload = payload



def create_configuration(arn:str=None, memory: list=None, invocations: int=None, payload:dict=None):
    return {
        "lambdaARN": arn,
        "powerValues": memory,
        "num": invocations,
        "payload": {} if not payload else payload
    }



def cleaner(invocations: int=None, arn:str=None):
    '''Delete all previous generated aliases and versions'''
    return [f'deleting {arn}/{invocation}...' for invocation in range(invocations)]

def analyzer():
    return

def optimize(configuration):
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