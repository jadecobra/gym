def create_input(arn=None, power_values=None, num=None, payload=None):
    return {
        "lambdaARN": arn,
        "powerValues": power_values,
        "num": num,
        "payload": {} if not payload else payload
    }