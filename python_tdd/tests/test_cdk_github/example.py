import aws_cdk
import aws_cdk.pipelines
import cdk_pipelines_github


app = aws_cdk.App()
pipeline = cdk_pipelines_github.GitHubWorkflow(
    app, 'Pipeline',
    synth=aws_cdk.pipelines.ShellStep(
        'Build',
        commands=[
            'yarn install',
            'yarn build',
        ],
    ),
    aws_creds=cdk_pipelines_github.AwsCredentials.from_open_id_connect(
        git_hub_action_role_arn=f'arn:aws:iam::{account_id}:role/GitHubActionRole',
    ),
)

pipeline.add_stage(pipelines.MySt)