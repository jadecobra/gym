import aws_cdk
import constructs
import cdk_pipelines_github


class EcsFlask(aws_cdk.Stack):

    def __init__(self, scope: constructs.Construct, construct_id: str,
        github_role_arn=None, **kwargs
    ) -> None:
        super().__init__(scope, construct_id, **kwargs)

        github_username = self.get_github_username()
        github_repository = self.get_github_repository()
        github_personal_token = self.get_personal_token()
        ecr_repository = self.create_ecr_repository()

        self.create_cluster_admin_role()
        cluster = self.create_cluster(self.get_vpc())
        task_definition = self.get_task_definition(self.create_task_role())
        task_definition.add_to_execution_role_policy(self.execution_role_policy())
        container = self.add_task_definition_container(
            task_definition=task_definition,
            logging=self.get_logging(),
        )
        self.add_port_mappings(container)
        fargate_service = self.create_fargate_service(
            cluster=cluster,
            task_definition=task_definition,
        )
        scaling = fargate_service.service.auto_scale_task_count(max_capacity=6)
        scaling.scale_on_cpu_utilization(
            'CpuScaling',
            target_utilization_percent=10,
            scale_in_cooldown=self.duration(),
            scale_out_cooldown=self.duration(),
        )
        self.create_github_workflow()
        # project = self.create_codebuild_project(
        #     source=self.get_source_code(
        #         owner=github_username.value_as_string,
        #         repository=github_repository.value_as_string,
        #     ),
        #     cluster_name=cluster.cluster_name,
        #     repository_url=ecr_repository.repository_uri,
        # )

        # source_output = self.create_artifact()
        # build_output = self.create_artifact()

        # self.create_code_pipeline(
        #     source_action=self.git_checkout(
        #         owner=github_username.value_as_string,
        #         repository=github_repository.value_as_string,
        #         personal_access_token=github_personal_token.value_as_string,
        #         source_output=source_output,
        #     ),
        #     build_action=self.code_build_action(
        #         project=project,
        #         source_output=source_output,
        #         build_output=build_output,
        #     ),
        #     manual_approval_action=self.manual_approval_action(),
        #     deploy_action=self.deploy_action(
        #         service=fargate_service.service,
        #         build_output=build_output,
        #     ),
        # )

        github_action_role = aws_cdk.aws_iam.Role.from_role_arn(
            self, 'GitHubActionRole',
            role_arn=github_role_arn
        )
        ecr_repository.grant_pull_push(github_action_role)
        self.add_role_policy(
            role=github_action_role,
            cluster_arn=cluster.cluster_arn,
        )

        aws_cdk.CfnOutput(self, "image", value=f'{ecr_repository.repository_uri}:latest')
        aws_cdk.CfnOutput(self, 'loadbalancerdns', value=fargate_service.load_balancer.load_balancer_dns_name)

    @staticmethod
    def add_role_policy(role=None, cluster_arn=None):
        return role.add_to_principal_policy(
            aws_cdk.aws_iam.PolicyStatement(
                actions=[
                    "ecs:describecluster",
                    "ecr:getauthorizationtoken",
                    "ecr:batchchecklayeravailability",
                    "ecr:batchgetimage",
                    "ecr:getdownloadurlforlayer"
                ],
                resources=[cluster_arn],
            )
        )

    @staticmethod
    def deploy_action(service=None, build_output=None):
        return aws_cdk.aws_codepipeline_actions.EcsDeployAction(
            action_name='deployAction',
            service=service,
            image_file=aws_cdk.aws_codepipeline.ArtifactPath(
                build_output,
                'imagedefinitions.json'
            )
        )

    @staticmethod
    def manual_approval_action():
        return aws_cdk.aws_codepipeline_actions.ManualApprovalAction(
            action_name='approve',
        )

    @staticmethod
    def code_build_action(project=None, source_output=None, build_output=None):
        return aws_cdk.aws_codepipeline_actions.CodeBuildAction(
            action_name='codebuild',
            project=project,
            input=source_output,
            outputs=[build_output], # optional
        )

    @staticmethod
    def git_checkout(owner=None, repository=None, source_output=None, personal_access_token=None):
        return aws_cdk.aws_codepipeline_actions.GitHubSourceAction(
            action_name='github_source',
            owner=owner,
            repo=repository,
            branch='main',
            oauth_token=aws_cdk.SecretValue.secrets_manager(personal_access_token),
            output=source_output
        )

    @staticmethod
    def create_artifact():
        return aws_cdk.aws_codepipeline.Artifact()

    @staticmethod
    def duration():
        return aws_cdk.Duration.seconds(60)


    def get_github_username(self):
        return aws_cdk.CfnParameter(
            self, "githubUserName",
            type="String",
            description="Github username for source code repository"
        )

    def get_github_repository(self):
        return aws_cdk.CfnParameter(
            self, "githubRespository",
            type="String",
            description="Github source code repository",
            default="amazon-ecs-fargate-cdk-v2-cicd"
        )

    def get_personal_token(self):
        return aws_cdk.CfnParameter(
            self, "githubPersonalTokenSecretName",
            type="String",
            description="The name of the AWS Secrets Manager Secret which holds the GitHub Personal Access Token for self project.",
            default="/aws-samples/amazon-ecs-fargate-cdk-v2-cicd/github/personal_access_token"
        )

    def create_ecr_repository(self):
        return aws_cdk.aws_ecr.Repository(self, 'EcrRepository')

    def get_vpc(self):
        return aws_cdk.aws_ec2.Vpc(
            self, 'Vpc',
            cidr='10.0.0.0/16',
            nat_gateways=1,
            max_azs=3
        )

    def create_cluster_admin_role(self):
        return aws_cdk.aws_iam.Role(
            self, 'ClusterAdminRole',
            assumed_by=aws_cdk.aws_iam.AccountRootPrincipal()
        )

    def create_cluster(self, vpc):
        return aws_cdk.aws_ecs.Cluster(
            self, "Cluster",
            vpc=vpc
        )

    def get_logging(self):
        return aws_cdk.aws_ecs.AwsLogDriver(
            stream_prefix="ecs-logs"
        )

    def create_task_role(self):
        return aws_cdk.aws_iam.Role(
            self, f'ecs-taskrole-{self.stack_name}',
            role_name=f'ecs-taskrole-{self.stack_name}',
            assumed_by=aws_cdk.aws_iam.ServicePrincipal('ecs-tasks.amazonaws.com')
        )

    def execution_role_policy(self):
        return aws_cdk.aws_iam.PolicyStatement(
            effect=aws_cdk.aws_iam.Effect.ALLOW,
            resources=['*'],
            actions=[
                "ecr:getauthorizationtoken",
                "ecr:batchchecklayeravailability",
                "ecr:getdownloadurlforlayer",
                "ecr:batchgetimage",
                "logs:createlogstream",
                "logs:putlogevents"
            ]
        )

    def get_task_definition(self, task_role):
        return aws_cdk.aws_ecs.FargateTaskDefinition(
            self, "TaskDefinition",
            task_role=task_role
        )

    def add_task_definition_container(self, task_definition=None, logging=None):
        return task_definition.add_container(
            'flask-app',
            image=aws_cdk.aws_ecs.ContainerImage.from_registry('public.ecr.aws/amazonlinux/amazonlinux:2022'),
            memory_limit_mib=256,
            cpu=256,
            logging=logging,
        )

    def add_port_mappings(self, container):
        return container.add_port_mappings(
            aws_cdk.aws_ecs.PortMapping(
                container_port=5000,
                protocol=aws_cdk.aws_ecs.Protocol.TCP
            )
        )

    def create_fargate_service(self, cluster=None, task_definition=None):
        return aws_cdk.aws_ecs_patterns.ApplicationLoadBalancedFargateService(
            self, "FargateService",
            cluster=cluster,
            task_definition=task_definition,
            public_load_balancer=True,
            desired_count=1,
            listener_port=80
        )

    def get_source_code(self, owner=None, repository=None):
        return aws_cdk.aws_codebuild.Source.git_hub(
            owner=owner,
            repo=repository,
            webhook=True, # optional, default: True if 'webhookfilteres' were provided, False otherwise
            webhook_filters=[
                aws_cdk.aws_codebuild.FilterGroup.in_event_of(
                    aws_cdk.aws_codebuild.EventAction.PUSH
                ).and_branch_is('main'),
            ], # optional, by default all pushes and pull requests will trigger a build
        )

    @staticmethod
    def build_commands():
        return [
            'cd flask-docker-app',
            'docker build -t $ecr_repo_uri:$tag .',
            '$(aws ecr get-login --no-include-email)',
            'docker push $ecr_repo_uri:$tag'
        ]

    @staticmethod
    def pre_build_commands():
        return [
            'env',
            'export tag=latest'
        ]

    @staticmethod
    def post_build_commands():
        return [
            'echo "in post-build stage"',
            'cd ..',
            "printf '[{\"name\":\"flask-app\",\"imageUri\":\"%s\"}]' $ecr_repo_uri:$tag > imagedefinitions.json",
            "pwd; ls -al; cat imagedefinitions.json"
        ]

    def get_build_spec(self):
        # TODO - I had to hardcode tag here
        return aws_cdk.aws_codebuild.BuildSpec.from_object({
            'version': "0.2",
            'phases': {
                'pre_build': {
                    '''
                    'commands': [
                        'env',
                        'export tag=${CODEBUILD_RESOLVED_SOURCE_VERSION}'
                    ]
                    '''
                    'commands': self.pre_build_commands()
                },
                'build': {
                    'commands': self.build_commands()
                },
                'post_build': {
                    'commands': self.post_build_commands()
                }
            },
            'artifacts': {
                'files': [
                    'imagedefinitions.json'
                ]
            }
        })

    def create_codebuild_project(self, source=None, cluster_name=None, repository_url=None):
        return aws_cdk.aws_codebuild.Project(
            self, 'CodeBuildProject',
            project_name=self.stack_name,
            source=source,
            environment=aws_cdk.aws_codebuild.BuildEnvironment(
                build_image=aws_cdk.aws_codebuild.LinuxBuildImage.AMAZON_LINUX_2_2,
                privileged=True
            ),
            environment_variables={
                'cluster_name': aws_cdk.aws_codebuild.BuildEnvironmentVariable(
                    value=cluster_name
                ),
                'ecr_repo_uri': aws_cdk.aws_codebuild.BuildEnvironmentVariable(
                    value=repository_url
                )
            },
            badge=True,
            build_spec=self.get_build_spec()
        )

    def create_github_workflow(self):
        # NOTE - Approve action is commented out!
        return cdk_pipelines_github.GitHubWorkflow(
            self, 'GitHubWorkflow',
            workflow_name='CI/CD Pipeline',
            workflow_path='.github/workflows/deploy.yml',
            pre_build_steps=[
                cdk_pipelines_github.JobStep(
                    run=command
                ) for command in self.pre_build_commands()
            ],
            synth=aws_cdk.pipelines.ShellStep(
                'Build',
                commands=self.build_commands()
            ),
            post_build_steps=[
                cdk_pipelines_github.JobStep(
                    run=command
                ) for command in self.post_build_commands()
            ],
            aws_creds=cdk_pipelines_github.AwsCredentials.from_open_id_connect(
                git_hub_action_role_arn='arn:aws:iam::<account-id>:role/GitHubActionRole'
            )
        )

    def create_code_pipeline(self, source_action=None, build_action=None, manual_approval_action=None, deploy_action=None):
        # NOTE - Approve action is commented out!
        return aws_cdk.aws_codepipeline.Pipeline(
            self, 'CodePipeline',
            stages=[
                aws_cdk.aws_codepipeline.StageProps(
                    stage_name='source',
                    actions=[source_action],
                ),
                aws_cdk.aws_codepipeline.StageProps(
                    stage_name='build',
                    actions=[build_action],
                ),
                aws_cdk.aws_codepipeline.StageProps(
                    stage_name='approve',
                    actions=[manual_approval_action],
                ),
                aws_cdk.aws_codepipeline.StageProps(
                    stage_name='deploy-to-ecs',
                    actions=[deploy_action],
                )
            ]
        )