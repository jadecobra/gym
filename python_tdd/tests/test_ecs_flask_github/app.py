#!/usr/bin/env python3
import aws_cdk
import ecs_flask
import github_role

app = aws_cdk.App()

github_action_role = github_role.GitHubActionRole(
    app, 'GitHubActionRole',
    env=aws_cdk.Environment(
        region=app.node.try_get_context('region'),
        account=app.node.try_get_context('account')
    )
)


ecs_flask.EcsFlask(
    app, "EcsFlask",
    github_role_arn=github_action_role.role.role_arn,
    env=aws_cdk.Environment(
        region=app.node.try_get_context('region'),
        account=app.node.try_get_context('account')
    )
)

app.synth()
