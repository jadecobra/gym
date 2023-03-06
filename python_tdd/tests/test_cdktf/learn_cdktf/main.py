#!/usr/bin/env python
import constructs
import cdktf
import cdktf_cdktf_provider_docker


class MyStack(cdktf.TerraformStack):

    def __init__(self, scope: constructs.Construct, id: str):
        super().__init__(scope, id)

        cdktf_cdktf_provider_docker.provider.DockerProvider(self, 'Docker')
        docker_image = cdktf_cdktf_provider_docker.image.Image(
            self, 'nginxImage',
            name='nginx:latest',
            keep_locally=False,
        )

        cdktf_cdktf_provider_docker.container.Container(
            self, 'nginxContainer',
            name='tutorial',
            image=docker_image.name,
            ports=[{
                'internal': 80,
                'external': 8000,
            }]
        )


app = cdktf.App()
MyStack(app, "learn_cdktf")

app.synth()
