import aws_cdk
import constructs
import cdk_pipelines_github


class GitHubActionRole(aws_cdk.Stack):

    def __init__(self, scope: constructs.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        self.role = cdk_pipelines_github.GitHubActionRole(
            self, 'github_action_role',
            repos=['jadecobra/gym'],
        ).role