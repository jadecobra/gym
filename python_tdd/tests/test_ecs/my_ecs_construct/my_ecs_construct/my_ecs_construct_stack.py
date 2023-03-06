import aws_cdk
import constructs

class MyEcsConstructStack(aws_cdk.Stack):

    def __init__(self, scope: constructs.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        vpc = aws_cdk.aws_ec2.Vpc(self, 'MyVpc', max_azs=3)

        cluster = aws_cdk.aws_ecs.Cluster(self, 'Cluster', vpc=vpc)

        aws_cdk.aws_ecs_patterns.ApplicationLoadBalancedFargateService(
            self, 'MyFargateService',
            cluster=cluster,
            cpu=512,
            desired_count=6,
            memory_limit_mib=2048,
            public_load_balancer=True,
            task_image_options=aws_cdk.aws_ecs_patterns.ApplicationLoadBalancedTaskImageOptions(
                image=aws_cdk.aws_ecs.ContainerImage.from_registry(
                    'amazon/amazon-ecs-sample'
                )
            ),
        )