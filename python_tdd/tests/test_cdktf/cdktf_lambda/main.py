#!/usr/bin/env python
import os
import constructs
import cdktf_cdktf_provider_aws


# from constructs import Construct
# from cdktf import App, TerraformStack


class MyStack(cdktf.TerraformStack):

    def __init__(self, scope: constructs.Construct, id: str):
        super().__init__(scope, id)

        # define resources here


app = cdktf.App()
MyStack(app, "cdktf_lambda")

app.synth()
