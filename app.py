#!/usr/bin/env python3
import os
import json
import boto3
import aws_cdk as cdk
from aws_cdk import (Tags)

from demo_bot.demo_bot_stack import DemoBotStack

secrets_client = boto3.client(service_name='secretsmanager')
instance_secrets = json.loads(secrets_client.get_secret_value( SecretId='instance_id')['SecretString'])
paramaters_secrets = json.loads(secrets_client.get_secret_value( SecretId='project_parameters')['SecretString'])

secrets = {**paramaters_secrets, **instance_secrets}

TAGS = json.loads(secrets['TAGS'])


app = cdk.App()
stk = DemoBotStack(app, "DemoBotStack", secrets
    # If you don't specify 'env', this stack will be environment-agnostic.
    # Account/Region-dependent features and context lookups will not work,
    # but a single synthesized template can be deployed anywhere.

    # Uncomment the next line to specialize this stack for the AWS Account
    # and Region that are implied by the current CLI configuration.

    #env=cdk.Environment(account=os.getenv('CDK_DEFAULT_ACCOUNT'), region=os.getenv('CDK_DEFAULT_REGION')),

    # Uncomment the next line if you know exactly what Account and Region you
    # want to deploy the stack to. */

    #env=cdk.Environment(account='123456789012', region='us-east-1'),

    # For more information, see https://docs.aws.amazon.com/cdk/latest/guide/environments.html
    )
if TAGS.keys():
    for k in TAGS.keys():
        Tags.of(stk).add(k, TAGS[k])

app.synth()
