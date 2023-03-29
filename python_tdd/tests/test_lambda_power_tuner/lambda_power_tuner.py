def create_configuration(arn=None, memory=None, number=None, payload=None):
    return {
        "lambdaARN": arn,
        "powerValues": memory,
        "num": number,
        "payload": {} if not payload else payload
    }

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