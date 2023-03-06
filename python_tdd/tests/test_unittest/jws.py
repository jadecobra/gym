import boto3

EC2 = boto3.client('ec2')

def describe_instances():
    return EC2.describe_instances()
