#!/usr/bin/env python
import constructs
import cdktf
import cdktf_cdktf_provider_aws


class MyStack(cdktf.TerraformStack):

    def __init__(self, scope: constructs.Construct, id: str):
        super().__init__(scope, id)

        # define resources here
        cdktf_cdktf_provider_aws.provider.AwsProvider(
            self, 'AWS',
            region='us-west-1',
        )

        instance = cdktf_cdktf_provider_aws.instance.Instance(
            self, 'compute',
            ami='ami-01456a894f71116f2',
            instance_type='t2.micro',
            tags={
                'Name': 'cdktf-demo'
            }
        )

        cdktf.TerraformOutput(
            self, 'public_ip',
            value=instance.public_ip,
        )


app = cdktf.App()
MyStack(app, "learn_cdktf_again")

app.synth()
