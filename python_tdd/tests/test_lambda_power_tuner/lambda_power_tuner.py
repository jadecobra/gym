def create_configuration(arn=None, memory=None, number=None, payload=None):
    return {
        "lambdaARN": arn,
        "powerValues": memory,
        "num": number,
        "payload": {} if not payload else payload
    }