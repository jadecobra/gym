import aws_cdk
import constructs


class HelloEcsStack(aws_cdk.Stack):

    def __init__(self, scope: constructs.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        aws_cdk.aws_ecs_patterns.ApplicationLoadBalancedFargateService(
            self, 'MyWebServer',
            task_image_options=aws_cdk.aws_ecs_patterns.ApplicationLoadBalancedTaskImageOptions(
                image=aws_cdk.aws_ecs.ContainerImage.from_registry('amazon/amazon-ecs-sample'),
                public_load_balancer=True
            )
        )