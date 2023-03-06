import aws_cdk
import cdk_pipelines_github_workflows

app = aws_cdk.App()
cdk_pipelines_github_workflows.CdkPipelinesGitHub(
    app, 'CdkPipelinesGitHub',
)
app.synth()