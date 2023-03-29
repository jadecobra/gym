def create_configuration(arn:str=None, memory: list=None, invocations: int=None, payload:dict=None):
    return {
        "lambdaARN": arn,
        "powerValues": memory,
        "num": invocations,
        "payload": {} if not payload else payload
    }

def initiator():
    '''Return N versions and aliases for each memory'''
    return

def executor():
    return

def cleaner():
    return

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